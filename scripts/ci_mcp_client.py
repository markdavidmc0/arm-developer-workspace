#!/usr/bin/env python3
"""
M2M Client Benchmark Script for Arm Developer Workspace
Zero-dependency Python script using urllib.request and json.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="M2M CI MCP Benchmark Client")
    parser.add_argument("--workload-path", required=True, help="Path to the modified workload directory")
    parser.add_argument("--endpoint-url", default=os.getenv("PLATFORM_ENDPOINT_URL", "https://mvcp-gateway.your-domain.com/api/v1/optimize"), help="Control Plane API endpoint")
    parser.add_argument("--api-key", default=os.getenv("ARM_M2M_API_KEY", ""), help="API Authorization Key")
    parser.add_argument("--mock", action="store_true", help="Force mock benchmark execution mode")
    parser.add_argument("--output-report", default="benchmark_report.md", help="Path to write the output markdown report")
    return parser.parse_args()


def normalize_domain_context(workload_path: str) -> str:
    """
    Parses workload_path to extract normalized domain context.
    e.g. 'workloads/04-physical-ai/ros2-pointcloud-voxel' -> 'physical-ai'
    e.g. 'workloads/01-cloud-ai/llamacpp-int4-dequant' -> 'cloud-ai'
    """
    parts = Path(workload_path).parts
    for part in parts:
        if part.startswith("workloads") or part == ".":
            continue
        # Strip leading numbers/hyphens e.g., '04-physical-ai' -> 'physical-ai'
        normalized = re.sub(r"^\d+-", "", part)
        if normalized:
            return normalized
    return "general"


def select_primary_source_file(workload_path: str) -> tuple[Path, str]:
    """
    Selects primary source file based on strict priority: .cpp -> .c -> .py -> first readable code file.
    Ignores markdown, build scripts, dotfiles, etc.
    """
    path = Path(workload_path)
    if not path.exists():
        raise FileNotFoundError(f"Workload directory '{workload_path}' does not exist.")

    files = [f for f in path.glob("*") if f.is_file() and not f.name.startswith(".")]
    
    # Priority extensions
    priorities = [".cpp", ".c", ".py"]
    for ext in priorities:
        for f in files:
            if f.suffix.lower() == ext and not f.name.lower().endswith(".md"):
                return f, f.read_text(encoding="utf-8", errors="replace")

    # Fallback to first non-doc code file
    ignored_extensions = {".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".cmake"}
    for f in files:
        if f.suffix.lower() not in ignored_extensions and f.name != "CMakeLists.txt":
            return f, f.read_text(encoding="utf-8", errors="replace")

    # Ultimate fallback if no code file found
    if files:
        f = files[0]
        return f, f.read_text(encoding="utf-8", errors="replace")
    
    raise FileNotFoundError(f"No valid source files found in workload directory '{workload_path}'.")


def generate_mock_report(workload_path: str, domain: str, source_filename: str, reason: str) -> str:
    return f"""<!-- arm-mcp-benchmark-marker -->
# 🦾 Arm M2M CI/CD Benchmark Report

> ℹ️ **Mode:** Dry-Run / Mock Benchmark Mode
> **Reason:** {reason}

### 📊 Performance Summary
* **Workload Directory:** `{workload_path}`
* **Target Domain:** `{domain}`
* **Source Analyzed:** `{source_filename}`
* **Execution Status:** ⚠️ Mock Evaluation Completed

| Metric | Baseline | Arm Neoverse / KleidiAI Optimized | Improvement |
| :--- | :--- | :--- | :--- |
| **Execution Time** | 12.45 ms | 2.81 ms | **4.43x Speedup** |
| **Vectorization** | Scalar Loops | SVE2 / NEON 128-bit Vectorized | Enabled |
| **Memory Bandwidth** | 4.2 GB/s | 1.1 GB/s | **73.8% Reduction** |
| **Cache Line Utilization** | 32% L1 hit rate | 89% L1 hit rate | **+57% Locality** |

### 💡 Suggested Optimizations Applied
- Applied `-march=armv9-a+sve2` compiler vectorization flags.
- Replaced scalar nested loops with Arm KleidiAI micro-kernel routines.
- Applied cache-line alignment to data arrays.

---
*Report generated automatically by Arm M2M Platform Control Plane CI/CD Pipeline.*
"""


def main():
    args = parse_args()
    domain = normalize_domain_context(args.workload_path)
    
    try:
        source_file, source_content = select_primary_source_file(args.workload_path)
        source_filename = source_file.name
    except Exception as e:
        print(f"Warning: Failed to resolve source file in {args.workload_path}: {e}", file=sys.stderr)
        source_filename = "unknown.cpp"
        source_content = "// Empty or unreadable source file"

    # Check if mock mode is forced or required due to missing API key
    if args.mock or not args.api_key:
        reason = "Explicit --mock flag set" if args.mock else "ARM_M2M_API_KEY secret not provided (e.g. fork PR or dry-run)"
        print(f"Executing in Mock Mode: {reason}")
        report = generate_mock_report(args.workload_path, domain, source_filename, reason)
        Path(args.output_report).write_text(report, encoding="utf-8")
        print(f"Successfully generated mock benchmark report at '{args.output_report}'.")
        return

    # Prepare REST API payload
    payload = {
        "workload": Path(args.workload_path).name,
        "domain": domain,
        "filename": source_filename,
        "code": source_content
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {args.api_key}",
        "X-Workspace-Context": domain,
        "User-Agent": "Arm-M2M-CI-Client/1.0"
    }

    req = urllib.request.Request(args.endpoint_url, data=data, headers=headers, method="POST")

    try:
        print(f"Sending M2M optimization benchmark request to {args.endpoint_url} (Domain Context: {domain})...")
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)

            report_md = res_json.get("markdown_report") or res_json.get("report")
            if not report_md:
                # Format fallback report from metrics
                speedup = res_json.get("speedup", "N/A")
                vector_status = res_json.get("vectorization", "Enabled")
                report_md = f"""<!-- arm-mcp-benchmark-marker -->
# 🦾 Arm M2M CI/CD Benchmark Report

### 📊 Performance Summary
* **Workload Directory:** `{args.workload_path}`
* **Target Domain:** `{domain}`
* **Source Analyzed:** `{source_filename}`
* **Speedup Achieved:** **{speedup}**
* **Vectorization:** `{vector_status}`

---
*Report generated automatically by Arm M2M Platform Control Plane CI/CD Pipeline.*
"""
            # Ensure tracking marker is present
            if "<!-- arm-mcp-benchmark-marker -->" not in report_md:
                report_md = "<!-- arm-mcp-benchmark-marker -->\n" + report_md

            Path(args.output_report).write_text(report_md, encoding="utf-8")
            print(f"Successfully wrote live benchmark report to '{args.output_report}'.")

    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as err:
        print(f"Warning: Communication with remote endpoint failed ({err}). Degrading gracefully to Mock Mode.", file=sys.stderr)
        report = generate_mock_report(args.workload_path, domain, source_filename, f"Control Plane Endpoint Unreachable ({err})")
        Path(args.output_report).write_text(report, encoding="utf-8")
        print(f"Successfully generated fallback mock report at '{args.output_report}'.")


if __name__ == "__main__":
    main()
