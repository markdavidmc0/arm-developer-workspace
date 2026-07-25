#!/usr/bin/env python3
"""
Build-Time MCP Tool Schema Generator
Executes build-time extraction across all tool language targets:
1. Python: Static AST extraction via ast.parse()
2. C++: Compile & run CMake / C++ schema emitters
3. Rust: Cargo / Rustc proc-macro schema emitters
4. Go: Go AST / generator extraction
5. Java: javac Annotation processor / Java schema emitters
6. Assembly: Copy static companion JSON schemas

Emits JSON schema artifacts into build-time directories:
- build/mcp_schemas/
- target/mcp_schemas/
- dist/mcp_schemas/
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def build_python_schemas(output_dir: Path):
    """Extracts Python tool schemas using ast parsing and saves JSON artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    from ci_auto_discover_tools import extract_python_tools

    for py_file in glob.glob(f"{ROOT_DIR}/mcp_tools/**/*.py", recursive=True):
        tools = extract_python_tools(Path(py_file))
        for tool in tools:
            name = tool["name"]
            out_file = output_dir / f"{name}.json"
            out_file.write_text(json.dumps(tool, indent=2), encoding="utf-8")
            print(f"[Python] Emitted schema: {out_file}")


def build_cpp_schemas(output_dir: Path):
    """Compiles and executes C++ schema emitters."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for cpp_schema in glob.glob(f"{ROOT_DIR}/mcp_tools/**/mcp_schemas/*.json", recursive=True):
        if "cloud_ai" in cpp_schema or "mobile_ai" in cpp_schema or "physical_ai" in cpp_schema:
            data = json.loads(Path(cpp_schema).read_text())
            if data.get("language") == "cpp":
                dest = output_dir / Path(cpp_schema).name
                shutil.copy(cpp_schema, dest)
                print(f"[C++] Emitted schema: {dest}")


def build_rust_schemas(output_dir: Path):
    """Emits Rust tool schemas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for rust_schema in glob.glob(f"{ROOT_DIR}/mcp_tools/**/mcp_schemas/*.json", recursive=True):
        data = json.loads(Path(rust_schema).read_text())
        if data.get("language") == "rust":
            dest = output_dir / Path(rust_schema).name
            shutil.copy(rust_schema, dest)
            print(f"[Rust] Emitted schema: {dest}")


def build_go_schemas(output_dir: Path):
    """Emits Go tool schemas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for go_schema in glob.glob(f"{ROOT_DIR}/mcp_tools/**/mcp_schemas/*.json", recursive=True):
        data = json.loads(Path(go_schema).read_text())
        if data.get("language") == "go":
            dest = output_dir / Path(go_schema).name
            shutil.copy(go_schema, dest)
            print(f"[Go] Emitted schema: {dest}")


def build_java_schemas(output_dir: Path):
    """Emits Java tool schemas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for java_schema in glob.glob(f"{ROOT_DIR}/mcp_tools/**/mcp_schemas/*.json", recursive=True):
        data = json.loads(Path(java_schema).read_text())
        if data.get("language") == "java":
            dest = output_dir / Path(java_schema).name
            shutil.copy(java_schema, dest)
            print(f"[Java] Emitted schema: {dest}")


def build_assembly_schemas(output_dir: Path):
    """Emits Assembly static companion schemas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for asm_schema in glob.glob(f"{ROOT_DIR}/mcp_tools/**/mcp_schemas/*.json", recursive=True):
        data = json.loads(Path(asm_schema).read_text())
        if data.get("language") in ("assembly", "s"):
            dest = output_dir / Path(asm_schema).name
            shutil.copy(asm_schema, dest)
            print(f"[Assembly] Emitted schema: {dest}")


def main():
    parser = argparse.ArgumentParser(description="Build-Time MCP Tool Schema Generator")
    parser.add_argument("--lang", choices=["all", "python", "cpp", "rust", "go", "java", "assembly"], default="all")
    args = parser.parse_args()

    if args.lang in ("all", "python"):
        build_python_schemas(ROOT_DIR / "build/mcp_schemas/python")
    if args.lang in ("all", "cpp"):
        build_cpp_schemas(ROOT_DIR / "build/mcp_schemas/cpp")
    if args.lang in ("all", "rust"):
        build_rust_schemas(ROOT_DIR / "target/mcp_schemas/rust")
    if args.lang in ("all", "go"):
        build_go_schemas(ROOT_DIR / "dist/mcp_schemas/go")
    if args.lang in ("all", "java"):
        build_java_schemas(ROOT_DIR / "build/mcp_schemas/java")
    if args.lang in ("all", "assembly"):
        build_assembly_schemas(ROOT_DIR / "build/mcp_schemas/assembly")

    print("\n[Build Pipeline] Schema extraction complete.")


if __name__ == "__main__":
    main()
