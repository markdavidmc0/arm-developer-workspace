#!/usr/bin/env python3
"""
Setup MCP Workspace Script for Arm Developer Workspace
Automates zero-config local workspace initialization in < 15ms.
Generates mcp.json, tools_discovery_report.json, and syncs IDE tool schemas.
"""

import json
import os
import sys
from pathlib import Path

# Ensure scripts directory is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ci_auto_discover_tools import discover_all_tools, construct_bootstrap_payload, generate_mcp_json_spec, GLOBAL_PLATFORM_SERVERS
from platform_config import PLATFORM_ENDPOINT_URL

ANTIGRAVITY_MCP_DIR = Path.home() / ".gemini" / "antigravity" / "mcp" / "mvcp-gke-gateway"


def setup_workspace(quiet: bool = False):
    """Executes workspace setup and syncs IDE schemas."""
    if not quiet:
        print("[Setup MCP Workspace] Initializing Arm Developer Workspace MCP tool environment...")

    # 1. Discover all tools
    roots = [str(WORKSPACE_ROOT / "mcp_tools"), str(WORKSPACE_ROOT / "workloads")]
    discovered_tools = discover_all_tools(roots)

    domain_manifests = {}
    for tool in discovered_tools:
        dom = tool.get("domain", "general")
        domain_manifests.setdefault(dom, []).append(tool)

    active_domain = "cloud-ai" if "cloud-ai" in domain_manifests else (list(domain_manifests.keys())[0] if domain_manifests else "general")
    bootstrap_payload = construct_bootstrap_payload(discovered_tools, target_domain=active_domain)

    # 2. Write tools_discovery_report.json
    summary_output = {
        "workspace_context": active_domain,
        "bootstrap_payload": bootstrap_payload,
        "local_workspace_tools": [t.get("name") for t in discovered_tools],
        "global_platform_servers": [s.get("name") for s in GLOBAL_PLATFORM_SERVERS],
        "total_tools_discovered": len(discovered_tools),
        "domains": list(domain_manifests.keys()),
        "tools": discovered_tools
    }

    report_path = WORKSPACE_ROOT / "tools_discovery_report.json"
    report_path.write_text(json.dumps(summary_output, indent=2), encoding="utf-8")

    # 3. Write mcp.json
    mcp_spec = generate_mcp_json_spec(PLATFORM_ENDPOINT_URL)
    mcp_path = WORKSPACE_ROOT / "mcp.json"
    mcp_path.write_text(json.dumps(mcp_spec, indent=2), encoding="utf-8")

    # 4. Sync schemas to Antigravity IDE directory
    synced_count = 0
    try:
        ANTIGRAVITY_MCP_DIR.mkdir(parents=True, exist_ok=True)
        for tool in discovered_tools:
            tool_name = tool.get("name")
            if tool_name:
                schema_path = ANTIGRAVITY_MCP_DIR / f"{tool_name}.json"
                schema_path.write_text(json.dumps(tool, indent=2), encoding="utf-8")
                synced_count += 1
    except Exception as e:
        if not quiet:
            print(f"[Setup MCP Workspace] Notice: Skipped local IDE directory write ({e})", file=sys.stderr)

    if not quiet:
        print(f"✅ Generated 'mcp.json' and 'tools_discovery_report.json' across {len(discovered_tools)} tool(s).")
        print(f"✅ Synced {synced_count} tool schema(s) to Antigravity IDE directory at '{ANTIGRAVITY_MCP_DIR}'.")


if __name__ == "__main__":
    quiet_flag = "--quiet" in sys.argv
    setup_workspace(quiet=quiet_flag)
