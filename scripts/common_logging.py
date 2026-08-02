#!/usr/bin/env python3
"""
Central Logging and Logfire / OpenTelemetry Tracing Infrastructure
Provides unified logging and platform performance telemetry tracking:
- Prompt Token Usage & Savings
- Execution Latency (ms)
- Model Turns per Journey
- Gateway & Sandbox Error Rates
- Prompt Cache Hit Rates
- System Infrastructure Metrics (CPU, Memory, Network)
"""

import logging
import os
import sys
import time

try:
    import logfire
    LOGFIRE_AVAILABLE = True
except ImportError:
    LOGFIRE_AVAILABLE = False


def setup_pipeline_logging(default_level: int = logging.INFO) -> logging.Logger:
    """Configures centralized logging for Arm Developer Workspace scripts."""
    logger = logging.getLogger("arm_ai_platform")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(default_level)
    return logger


def setup_platform_telemetry(service_name: str = "arm-ai-platform"):
    """
    Initializes Logfire / OpenTelemetry tracing.
    Works seamlessly via `uv run logfire auth` local session OR `LOGFIRE_TOKEN` in CI/CD.
    """
    if LOGFIRE_AVAILABLE:
        try:
            # logfire.configure() uses active `logfire auth` credentials or LOGFIRE_TOKEN env var automatically
            logfire.configure(service_name=service_name)
            
            # Instrument host infrastructure metrics (CPU, RAM, Network) if system-metrics extra is present
            if hasattr(logfire, "instrument_system_metrics"):
                try:
                    logfire.instrument_system_metrics()
                except Exception as sys_err:
                    print(f"[Telemetry] Notice: System metrics instrumentation: {sys_err}", file=sys.stderr)

            print(f"[Telemetry] Logfire OpenTelemetry tracing initialized for service '{service_name}'.")
            return True
        except Exception as e:
            print(f"[Telemetry] Notice: Running in Local Mode ({e}). Metrics printed to stdout.", file=sys.stderr)
            return False
    else:
        print("[Telemetry] Notice: Logfire package not installed. Metrics printed to stdout.", file=sys.stderr)
        return False


def record_journey_metrics(
    journey_name: str,
    execution_mode: str,
    prompt_tokens: int,
    model_turns: int,
    latency_ms: float,
    error_count: int = 0,
    prompt_cache_hit: bool = True
) -> dict:
    """
    Records and formats user journey execution metrics.
    Optionally streams to Logfire if configured.
    """
    metrics = {
        "journey_name": journey_name,
        "execution_mode": execution_mode,
        "prompt_tokens": prompt_tokens,
        "model_turns": model_turns,
        "latency_ms": round(latency_ms, 2),
        "error_count": error_count,
        "prompt_cache_hit": prompt_cache_hit,
        "timestamp": time.time()
    }

    if LOGFIRE_AVAILABLE:
        try:
            logfire.info(
                "User Journey Executed: {journey_name} [{execution_mode}]",
                **metrics
            )
        except Exception:
            pass

    return metrics


def flush_telemetry():
    """Flushes all pending Logfire OpenTelemetry spans before process exit."""
    if LOGFIRE_AVAILABLE:
        try:
            if hasattr(logfire, "flush"):
                logfire.flush()
                print("[Telemetry] Successfully flushed all telemetry spans to Logfire.")
        except Exception as e:
            print(f"[Telemetry] Notice: Telemetry flush: {e}", file=sys.stderr)
