#!/usr/bin/env python3
"""
Zero-Regex Tool Auto-Discovery Script for Arm Developer Workspace
Scans both mcp_tools/ and workloads/ directories recursively.
Strict Architectural Directive:
- Python (.py): Standard library ast module (ast.parse, ast.walk) only.
- C / C++ / Rust / Go / Assembly / Java: Build artifacts / schema JSON files.
- REGEX USAGE: ZERO.
"""

import argparse
import ast
import glob
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Zero-Regex Multi-Language Tool Auto-Discovery Script")
    parser.add_argument("--roots", nargs="+", default=["mcp_tools", "workloads"], help="Root directories to scan")
    parser.add_argument("--endpoint-url", default=os.getenv("PLATFORM_ENDPOINT_URL", "https://mvcp-gateway.your-domain.com/api/v1/registry/register"), help="Registry registration endpoint")
    parser.add_argument("--api-key", default=os.getenv("ARM_M2M_API_KEY", ""), help="API Authorization Key")
    parser.add_argument("--mock", action="store_true", help="Force mock registration mode")
    parser.add_argument("--output-report", default="tools_discovery_report.json", help="Path to write output discovery manifest")
    return parser.parse_args()


def normalize_domain_context(path_str: str) -> str:
    """
    Parses directory path using Path.parts to extract normalized domain context.
    e.g. 'mcp_tools/cloud_ai/vllm_arm_kv...' -> 'cloud-ai'
    e.g. 'workloads/_template/tools_example...' -> 'template'
    """
    parts = Path(path_str).parts
    for part in parts:
        if part in (".", "mcp_tools", "workloads", "build", "target", "dist", "mcp_schemas"):
            continue
        cleaned = part.lstrip("_")
        if "-" in cleaned:
            prefix, rest = cleaned.split("-", 1)
            if prefix.isdigit():
                cleaned = rest
        cleaned = cleaned.replace("_", "-")
        return cleaned
    return "general"


def extract_python_tools(file_path: Path) -> list[dict]:
    """
    Extracts Python tools natively using standard library ast module.
    No execution, no regex.
    """
    tools = []
    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(file_path))
    except Exception as e:
        print(f"Warning: Failed to parse AST for {file_path}: {e}", file=sys.stderr)
        return tools

    domain = normalize_domain_context(str(file_path))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            is_mcp_tool = node.name.startswith("mcp__")

            for decorator in node.decorator_list:
                dec_name = ""
                if isinstance(decorator, ast.Name):
                    dec_name = decorator.id
                elif isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name):
                        dec_name = decorator.func.id
                    elif isinstance(decorator.func, ast.Attribute):
                        dec_name = decorator.func.attr
                elif isinstance(decorator, ast.Attribute):
                    dec_name = decorator.attr

                if dec_name in ("tool", "mcp", "mcp_tool", "McpTool") or "tool" in dec_name:
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

                tools.append({
                    "name": node.name,
                    "description": docstring,
                    "domain": domain,
                    "language": "python",
                    "source_file": str(file_path),
                    "parameters": {
                        "type": "object",
                        "properties": params
                    }
                })

    return tools


def discover_all_tools(roots: list[str]) -> list[dict]:
    """
    Two-Pass Tool Discovery Engine (Zero Regex):
    PASS 1: Python Static AST Discovery via ast module across scan roots.
    PASS 2: Compiled & Companion Schema Artifact Discovery (C++, Rust, Go, Java, Assembly).
    """
    discovered_tools = []

    # PASS 1: Python Static AST Discovery
    for root in roots:
        if not os.path.exists(root):
            continue
        for py_file in glob.glob(f"{root}/**/*.py", recursive=True):
            discovered_tools.extend(extract_python_tools(Path(py_file)))

    # PASS 2: Compiled Schema Artifact Discovery
    artifact_patterns = []
    for root in roots:
        artifact_patterns.extend([
            f"{root}/**/mcp_schemas/*.json",
            f"{root}/**/mcp_schemas/*.mcp.json",
            f"{root}/**/build/mcp_schemas/*.json",
            f"{root}/**/target/mcp_schemas/*.json",
            f"{root}/**/dist/mcp_schemas/*.json",
        ])

    found_files = set()
    for pattern in artifact_patterns:
        for json_file in glob.glob(pattern, recursive=True):
            found_files.add(json_file)

    for json_file in found_files:
        try:
            content = Path(json_file).read_text(encoding="utf-8", errors="replace")
            data = json.loads(content)
            domain = normalize_domain_context(json_file)

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "name" in item:
                        item.setdefault("domain", domain)
                        item.setdefault("source_file", json_file)
                        if not any(t["name"] == item["name"] for t in discovered_tools):
                            discovered_tools.append(item)
            elif isinstance(data, dict) and "name" in data:
                data.setdefault("domain", domain)
                data.setdefault("source_file", json_file)
                if not any(t["name"] == data["name"] for t in discovered_tools):
                    discovered_tools.append(data)
        except Exception as e:
            print(f"Warning: Failed to load artifact JSON at {json_file}: {e}", file=sys.stderr)

    return discovered_tools


def main():
    args = parse_args()
    discovered_tools = discover_all_tools(args.roots)

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
