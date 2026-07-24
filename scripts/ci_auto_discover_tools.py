#!/usr/bin/env python3
"""
Zero-Manifest Tool Auto-Discovery Script for Arm Developer Workspace
Zero-dependency Python script using ast, glob, json, urllib.request, and os.
Discovers MCP tools via:
1. Python AST inspection (@mcp.tool(), @tool, or mcp__ prefix).
2. Compiled language build schema sidecars (build/mcp_schemas/*.json).
"""

import argparse
import ast
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Zero-Manifest Tool Auto-Discovery Script")
    parser.add_argument("--workload-root", default="workloads", help="Root workloads directory to scan")
    parser.add_argument("--endpoint-url", default=os.getenv("PLATFORM_ENDPOINT_URL", "https://mvcp-gateway.your-domain.com/api/v1/registry/register"), help="Registry registration endpoint")
    parser.add_argument("--api-key", default=os.getenv("ARM_M2M_API_KEY", ""), help="API Authorization Key")
    parser.add_argument("--mock", action="store_true", help="Force mock registration mode")
    parser.add_argument("--output-report", default="tools_discovery_report.json", help="Path to write output discovery manifest")
    return parser.parse_args()


def normalize_domain_context(path_str: str) -> str:
    """
    Parses directory path to extract normalized domain context.
    e.g. 'workloads/04-physical-ai/ros2-pointcloud-voxel' -> 'physical-ai'
    e.g. 'workloads/01-cloud-ai' -> 'cloud-ai'
    """
    parts = Path(path_str).parts
    for part in parts:
        if part.startswith("workloads") or part == ".":
            continue
        normalized = re.sub(r"^\d+-", "", part)
        if normalized:
            return normalized
    return "general"


def extract_python_ast_tools(py_file_path: Path) -> list[dict]:
    """
    Parses a Python file using AST to extract functions decorated with
    @mcp.tool(), @tool, or prefixed with mcp__.
    """
    tools = []
    try:
        source = py_file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(py_file_path))
    except Exception as e:
        print(f"Warning: Failed to parse AST for {py_file_path}: {e}", file=sys.stderr)
        return tools

    domain = normalize_domain_context(str(py_file_path))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            is_mcp_tool = False
            
            # Check function prefix
            if node.name.startswith("mcp__"):
                is_mcp_tool = True

            # Check decorators
            for decorator in node.decorator_list:
                dec_str = ""
                if isinstance(decorator, ast.Name):
                    dec_str = decorator.id
                elif isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name):
                        dec_str = decorator.func.id
                    elif isinstance(decorator.func, ast.Attribute):
                        dec_str = decorator.func.attr
                elif isinstance(decorator, ast.Attribute):
                    dec_str = decorator.attr

                if dec_str in ("tool", "mcp_tool") or "tool" in dec_str:
                    is_mcp_tool = True
                    break

            if is_mcp_tool:
                docstring = ast.get_docstring(node) or f"MCP tool function {node.name}"
                params = {}
                for arg in node.args.args:
                    if arg.arg in ("self", "cls"):
                        continue
                    annotation = "string"
                    if arg.annotation and isinstance(arg.annotation, ast.Name):
                        annotation = arg.annotation.id
                    params[arg.arg] = {
                        "type": annotation,
                        "description": f"Parameter {arg.arg}"
                    }

                tool_schema = {
                    "name": node.name,
                    "description": docstring,
                    "domain": domain,
                    "language": "python",
                    "source_file": str(py_file_path),
                    "parameters": {
                        "type": "object",
                        "properties": params
                    }
                }
                tools.append(tool_schema)

    return tools


def scan_build_schema_sidecars(workload_root: str) -> list[dict]:
    """
    Scans build output directories for pre-emitted native MCP schema sidecars.
    e.g. build/mcp_schemas/*.json or workloads/**/mcp_schemas/*.json
    """
    sidecar_tools = []
    patterns = [
        os.path.join(workload_root, "**", "mcp_schemas", "*.json"),
        os.path.join(workload_root, "**", "build", "*.json"),
        os.path.join("build", "mcp_schemas", "*.json"),
        os.path.join("target", "mcp_schemas", "*.json")
    ]

    found_files = set()
    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            found_files.add(filepath)

    for filepath in found_files:
        try:
            content = Path(filepath).read_text(encoding="utf-8", errors="replace")
            data = json.loads(content)
            domain = normalize_domain_context(filepath)
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "name" in item:
                        item.setdefault("domain", domain)
                        item.setdefault("source_file", filepath)
                        sidecar_tools.append(item)
            elif isinstance(data, dict) and "name" in data:
                data.setdefault("domain", domain)
                data.setdefault("source_file", filepath)
                sidecar_tools.append(data)
        except Exception as e:
            print(f"Warning: Failed to parse sidecar JSON at {filepath}: {e}", file=sys.stderr)

    return sidecar_tools


def main():
    args = parse_args()
    root_path = Path(args.workload_root)

    if not root_path.exists():
        print(f"Error: Workload root path '{args.workload_root}' does not exist.", file=sys.stderr)
        sys.exit(1)

    discovered_tools = []

    # 1. AST Scan for Python files
    for py_file in root_path.rglob("*.py"):
        tools = extract_python_ast_tools(py_file)
        discovered_tools.extend(tools)

    # 2. Sidecar Scan for Native C++/C/Rust compiled schemas
    sidecar_tools = scan_build_schema_sidecars(args.workload_root)
    discovered_tools.extend(sidecar_tools)

    # Group tools by domain
    domain_manifests = {}
    for tool in discovered_tools:
        dom = tool.get("domain", "general")
        domain_manifests.setdefault(dom, []).append(tool)

    summary_output = {
        "total_tools_discovered": len(discovered_tools),
        "domains": list(domain_manifests.keys()),
        "tools": discovered_tools
    }

    Path(args.output_report).write_text(json.dumps(summary_output, indent=2), encoding="utf-8")
    print(f"Discovered {len(discovered_tools)} MCP tools across {len(domain_manifests)} domain(s). Report saved to '{args.output_report}'.")

    # Registration phase
    if args.mock or not args.api_key:
        print("Notice: Executing in Mock/Dry-Run Registration Mode (API Key missing or --mock flag set).")
        print(json.dumps(summary_output, indent=2))
        return

    # Post to Gateway per domain slice
    for domain, tools in domain_manifests.items():
        payload = json.dumps({"tools": tools}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {args.api_key}",
            "X-Workspace-Context": domain,
            "User-Agent": "Arm-M2M-AutoDiscover/1.0"
        }
        req = urllib.request.Request(args.endpoint_url, data=payload, headers=headers, method="POST")

        try:
            print(f"Registering {len(tools)} tool(s) for domain '{domain}' at {args.endpoint_url}...")
            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode("utf-8")
                print(f"Successfully registered domain '{domain}': {res_body}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as err:
            print(f"Warning: Failed to register tools for domain '{domain}': {err}. Continuing...", file=sys.stderr)


if __name__ == "__main__":
    main()
