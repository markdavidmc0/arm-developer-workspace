# AGENTS.md — Arm Developer Workspace (`arm-developer-workspace`)

This document establishes mandatory coding standards, architectural patterns, and execution verification steps for developers and AI agents operating on this repository.

---

## 🤖 AI Agent Operating Rules
1. **Mandatory Pre-Commit Verification:** Always run `uv run ruff check` and `uv run python scripts/ci_auto_discover_tools.py` before declaring a task finished.
2. **Assertion Safeguard:** Never modify or delete existing test assertions or tool schemas to make broken code pass.
3. **Documentation Compliance:** Write strict Google-style docstrings for all new tool modules and discovery functions.

---

## 📂 Key Repository Paths
* `mcp_tools/` — Python and multi-language tool packages (`cloud_ai/`, `physical_ai/`, `security/`).
* `workloads/` — Example benchmarking workloads and platform validation suites.
* `scripts/` — Tool auto-discovery and Keycloak OIDC pipeline scripts (`ci_auto_discover_tools.py`).
* `.github/workflows/` — CI/CD workflows (`publish_tools.yml`).

---

## 🐍 1. Environment, Tooling & Quality Standards
* **`uv` Package Management:** Use `uv` exclusively for environment management, dependency resolution, and execution. Never run direct `pip` commands.
  * Sync environment: `uv sync`
  * Add dependency: `uv add "package_name"`
  * Run tool auto-discovery: `uv run python scripts/ci_auto_discover_tools.py`
* **Linting & Formatting:** Run `uv run ruff check` and `uv run ruff format` to ensure strict PEP 8 and code-quality compliance.

---

## 🛠️ 2. Tool Discovery & Multi-Language Tool Authoring
* **Zero-Regex Tool Auto-Discovery:**
  * Store multi-language tools in `mcp_tools/` or `workloads/`.
  * Python tools use standard library `ast` parsing for tool annotations (`@mcp.tool` or `@tool`).
  * C++, Rust, Go, and Java tools output JSON schemas in `mcp_schemas/*.json` build artifacts.
* **Fail-Fast Error Handling in CI:**
  * Tool discovery scripts (`ci_auto_discover_tools.py`) must exit with non-zero status (`sys.exit(1)`) if registration endpoints respond with HTTP errors or if schema validation fails.
  * Do NOT swallow registration network errors silently.

---

## 📦 3. OCI Tool Container Publishing Standards
* **Multi-Architecture Arm64 Container Builds:**
  * All workspace tools are packaged via `Dockerfile.tools` into Arm64 OCI container images (`us-central1-docker.pkg.dev/sovereign-ai-495715/mcp-tools/arm-workspace-tools:latest`).
  * GitHub Actions workflows (`publish_tools.yml`) use QEMU and Buildx for cross-platform Arm64 compilation (`platforms: linux/arm64`).

---

## 🏗️ 4. Secretless OIDC GitHub Actions CI/CD
* **Secretless OIDC Authentication:**
  * Workflows must authenticate to GCP via `google-github-actions/auth@v2` using Workload Identity Federation (`mvcp-github-ci-sa@sovereign-ai-495715.iam.gserviceaccount.com`).
  * Never store static GCP JSON service account keys in GitHub Secrets.
  * Docker authentication against GCP Artifact Registry is configured via `gcloud auth configure-docker us-central1-docker.pkg.dev --quiet`.
