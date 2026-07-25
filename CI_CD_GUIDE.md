# M2M CI/CD Benchmarking & Optimization Pipeline Guide

This repository (`arm-developer-workspace`) hosts Arm-optimized workloads and domain-specific MCP tools across **Cloud AI**, **Mobile AI**, **Physical AI**, and **Security**.

---

## 🏗️ Architectural Model

The platform uses a **Domain-First Architecture** with a simple, pragmatic CI discovery strategy:

* **Domain MCP Tools (`mcp_tools/`)**: Custom domain utilities organized under `cloud_ai`, `mobile_ai`, `physical_ai`, and `security`.
* **Target Workloads (`workloads/`)**: Benchmarking source code, test kernels, and workload templates.

---

## ⚡ Tool Authoring & CI Discovery Strategy

To ensure CI runs fast without requiring heavy multi-gigabyte build toolchains (GCC/Clang, Cargo, Go SDK, JDK) installed in lightweight runner environments:

1. **Python Tools (`.py`)**:
   - Decorated with `@mcp.tool()` or `@tool`.
   - Extracted natively via standard library AST parsing (`ast.parse()`).
   - Zero JSON schema files required.

2. **Compiled Languages (C++, Rust, Go, Java, Assembly)**:
   - Native source code functions and driver implementations reside in tool directories.
   - Tool schemas are maintained as lightweight companion JSON files (`mcp_schemas/*.json`).
   - Enables fast, deterministic zero-dependency CI discovery in under **100ms**!

---

## 🔍 Running Auto-Discovery Locally

To run a discovery sweep across all domains:

```bash
python3 scripts/ci_auto_discover_tools.py --mock
```

---

## 👥 GitHub Codeowners

Domain directories map to specialized Arm engineering teams in `.github/CODEOWNERS`:

```text
mcp_tools/cloud_ai/      @Arm-Software/cloud-ai-team
mcp_tools/mobile_ai/     @Arm-Software/mobile-ai-team
mcp_tools/physical_ai/   @Arm-Software/physical-ai-team
mcp_tools/security/      @Arm-Software/security-team
```
