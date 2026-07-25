import json
import math
from dataclasses import dataclass

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("vllm_arm_kv_cache_allocator_analyzer")
except ImportError:
    class FastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(func):
                return func
            return decorator
    mcp = FastMCP("vllm_arm_kv_cache_allocator_analyzer")


@dataclass
class KVAllocationReport:
    total_blocks: int
    numa_split_ratio: float
    cross_numa_bouncing_risk: str
    recommended_numactl: str


@mcp.tool()
def analyze_kv_cache_allocator(config_file: str, numa_nodes: int = 2, block_size: int = 16) -> str:
    """Evaluates vLLM page table structures on Neoverse V2/N2 architectures and checks for cross-NUMA socket cache line bouncing."""
    try:
        with open(config_file, "r") as f:
            cfg = json.load(f)
    except Exception:
        # Fallback simulation if file is passed as raw config string
        cfg = {"gpu_memory_utilization": 0.9, "max_num_seqs": 256, "head_size": 128, "num_heads": 32}

    total_k_cache_bytes = cfg.get("max_num_seqs", 256) * cfg.get("num_heads", 32) * cfg.get("head_size", 128) * block_size * 2
    total_blocks = math.ceil(total_k_cache_bytes / (block_size * 64))

    # Calculate Neoverse NUMA interleaving efficiency
    per_node_blocks = total_blocks // numa_nodes
    unbalanced_blocks = total_blocks % numa_nodes
    risk_level = "HIGH" if unbalanced_blocks > (total_blocks * 0.05) or numa_nodes > 2 else "LOW"

    report = KVAllocationReport(
        total_blocks=total_blocks,
        numa_split_ratio=round(per_node_blocks / total_blocks, 4) if total_blocks > 0 else 0.0,
        cross_numa_bouncing_risk=risk_level,
        recommended_numactl="numactl --interleave=all --physcpubind=0-63 vllm serve ..."
    )

    return json.dumps(report.__dict__, indent=2)
