#!/usr/bin/env python3
"""
Arm AI Platform User Scenario Registry
Defines problem-first user scenarios with target success criteria.
Tool selection is left completely open so agents autonomously discover tools via the Central Registry.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class BenchmarkScenario:
    id: str
    domain: str
    title: str
    problem_prompt: str
    success_criteria: str


# Scenario Registry without hardcoded required tools
ALL_SCENARIOS: List[BenchmarkScenario] = [
    BenchmarkScenario(
        id="cloud-ai-vllm",
        domain="cloud-ai",
        title="Neoverse V2 SVE2 & vLLM NUMA Memory Optimization",
        problem_prompt=(
            "Our vLLM inference engine running on Neoverse V2 suffers from high p95 tail latencies "
            "during PyTorch model compilation and NUMA page allocation across 2 nodes. "
            "Diagnose hardware instruction latencies, inspect Inductor backend guards, "
            "and determine optimal NUMA core pinning."
        ),
        success_criteria="Identify SVE2 FMMLA latency, opt_level=3 Inductor guards, and 16-block NUMA allocation."
    ),
    BenchmarkScenario(
        id="physical-ai-zenoh",
        domain="physical-ai",
        title="ROS 2 Zenoh DDS & ISO 26262 ASIL-D Safety Verification",
        problem_prompt=(
            "An autonomous vehicle perception stack on Arm Cortex-A78AE experiences packet dropped frames "
            "over ROS 2 Zenoh DDS transport and hardware stalls. Profile transport latency and verify "
            "Embedded Trace Macrocell (ETM) execution traces against ISO 26262 ASIL-D safety rules."
        ),
        success_criteria="Detect Zenoh DDS queue stalls and verify ASIL-D ETM trace compliance."
    ),
    BenchmarkScenario(
        id="edge-ai-cortexm",
        domain="edge-ai",
        title="Cortex-M SRAM Footprint & Ethos-U NPU Cycle Estimation",
        problem_prompt=(
            "A micro-keyword spotting CNN model running on Cortex-M55 + Ethos-U55 NPU exceeds memory constraints. "
            "Calculate static SRAM footprint, evaluate layer quantization, and estimate NPU execution cycle budget."
        ),
        success_criteria="Verify SRAM footprint fits within 256KB constraint and compute NPU cycle budget."
    )
]


def load_all_scenarios() -> List[BenchmarkScenario]:
    """Returns list of registered user scenarios."""
    return ALL_SCENARIOS
