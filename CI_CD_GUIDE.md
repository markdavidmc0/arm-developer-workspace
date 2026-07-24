# 🚀 M2M CI/CD Benchmarking & Tool Discovery Guide

This guide details how workload contributors and platform engineers utilize the automated **Machine-to-Machine (M2M) CI/CD Benchmarking & Zero-Manifest Tool Discovery Pipeline** in this repository.

---

## 🏗️ Architectural Conceptual Model & Separation of Concerns

To maintain platform clarity, strictly adhere to this separation of concerns:
* **Domain MCP Tools (Actions)**: Custom domain-specific utilities defined in Python via `@mcp.tool()` or compiled C++/C/Rust schema sidecars (`build/mcp_schemas/*.json`). These tools are discovered and registered automatically into the central Gateway via `/api/v1/registry/register`.
* **Target Workloads (Data/Artifacts)**: Source code files (`.cpp`, `.c`, `.py` kernels) being evaluated or optimized. Target files are **never** registered as MCP tools—they are passed as payload arguments to `/api/v1/optimize`.

```
                  +-----------------------------------+
                  |  Pull Request / Push (workloads)  |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |  GitHub Actions Pipeline (.yml)   |
                  +-----------------------------------+
                   /                                 \
                  /                                   \
                 v                                     v
  +------------------------------+     +-------------------------------+
  | Step A: Tool Auto-Discovery  |     | Step C: M2M Benchmark Client  |
  | (scripts/ci_auto_discover)   |     | (scripts/ci_mcp_client.py)    |
  | - Python AST AST inspection  |     | - Resolves C++/Python target  |
  | - Native JSON build sidecars |     | - Normalizes domain context   |
  +------------------------------+     +-------------------------------+
                 |                                     |
                 v                                     v
  +------------------------------+     +-------------------------------+
  | POST /api/v1/registry/register|    | POST /api/v1/optimize         |
  +------------------------------+     +-------------------------------+
                                                       |
                                                       v
                                       +-------------------------------+
                                       | Sticky PR Comment Update      |
                                       | <!-- arm-mcp-benchmark-marker |
                                       +-------------------------------+
```

---

## 🛠️ Local Execution & Developer Quickstart

Engineers can run both helper scripts locally using standard Python (zero `pip install` required).

### 1. Test Zero-Manifest Tool Auto-Discovery
```bash
python3 scripts/ci_auto_discover_tools.py --mock
```
This scans `workloads/` for `@mcp.tool()` / `mcp__` Python AST definitions and `build/mcp_schemas/*.json` sidecars, outputting discovered MCP tool schemas locally.

### 2. Test M2M Benchmark Submission Client
```bash
python3 scripts/ci_mcp_client.py \
  --workload-path workloads/04-physical-ai/ros2-pointcloud-voxel \
  --mock
```
This evaluates the workload kernel locally in dry-run mode and writes `benchmark_report.md`.

---

## 👥 How Contributors Add a Workload or MCP Tool

1. **Pick a Priority Area**:
   - `workloads/00-foundations/`
   - `workloads/01-cloud-ai/`
   - `workloads/02-mobile-ai/`
   - `workloads/03-hardware-and-systems/`
   - `workloads/04-physical-ai/`

2. **Add Source Kernels**:
   Add your C++ (`.cpp`), C (`.c`), or Python (`.py`) code file inside your workload directory.

3. **Expose Domain Tools (Optional)**:
   - For Python: Decorate helper functions with `@mcp_tool` or prefix them with `mcp__`.
   - For Compiled C++/Rust: Generate JSON sidecars during build into `build/mcp_schemas/<tool_name>.json`.

4. **Open a Pull Request**:
   Push your branch and open a PR. The CI pipeline will automatically discover tools, register them with the Gateway, benchmark target kernels, and post a sticky performance comment on your PR!

---

## 🔑 Administrator Secret Management

To connect the GitHub Actions workflow to a live GCP Tau T2A Control Plane:

1. Navigate to **Settings ➡️ Secrets and variables ➡️ Actions** in your GitHub repository.
2. Add the following **Repository Secrets**:
   - `ARM_M2M_API_KEY`: The M2M authentication key issued by your Arm Control Plane gateway.
   - `PLATFORM_ENDPOINT_URL`: The REST API endpoint URL (e.g., `https://mvcp-gateway.your-domain.com`).

> ℹ️ **Fork Security:** Pull requests submitted from external forks do not have access to Repository Secrets by design. The CI workflow automatically detects this and gracefully falls back to `--mock` dry-run evaluation.
