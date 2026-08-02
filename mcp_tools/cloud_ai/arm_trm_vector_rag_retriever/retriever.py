import json
import math
import sys

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("arm_trm_vector_rag_retriever")
except ImportError:
    class FastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(func):
                return func
            return decorator
    mcp = FastMCP("arm_trm_vector_rag_retriever")


# In-Memory Vector Database KB containing vector embeddings for Arm TRMs & Silicon Errata
ARM_KNOWLEDGE_BASE = [
    {
        "id": "trm-neoverse-v2-sve2-01",
        "title": "Neoverse V2 SVE2 FMMLA Pipeline Latency & Throughput",
        "document": "Neoverse V2 cores feature dual 256-bit SVE2 vector pipelines. The FMMLA (Floating-point Matrix Multiply-Accumulate) instruction operates on 2x2 matrix tiles with 4-cycle execution latency and 1-cycle issue throughput per vector pipe. Optimal register tiling uses 8 z-registers to avoid pipeline stalls.",
        "category": "Architecture TRM",
        "vector_embedding": [0.82, 0.14, 0.95, 0.41, 0.12]
    },
    {
        "id": "errata-cortex-x3-alloc-42",
        "title": "Cortex-X3 Errata #2419082: SVE Vector Allocation Speculation",
        "document": "Speculative SVE vector register allocation on Cortex-X3 under heavy dynamic predicate changes can cause micro-op queue stalls. Workaround: Insert 'ptrue p0.b' predicate initialization outside hot loops or compile with '-fno-speculative-vector-alloc'.",
        "category": "Silicon Errata",
        "vector_embedding": [0.21, 0.91, 0.33, 0.88, 0.05]
    },
    {
        "id": "trm-graviton4-numa-03",
        "title": "AWS Graviton4 (Neoverse V2) NUMA Topology & Memory Interconnect",
        "document": "Graviton4 features 96 Neoverse V2 cores arranged in a unified System Guidance for Infrastructure (SGI) mesh. To achieve peak 530 GB/s memory bandwidth, pin NUMA threads using 'numactl --cpunodebind=0 --membind=0' and set 'topologySpreadConstraints' in Kubernetes manifests.",
        "category": "Cloud Optimization",
        "vector_embedding": [0.75, 0.32, 0.81, 0.19, 0.64]
    },
    {
        "id": "trm-kleidiai-u8s8-04",
        "title": "Arm KleidiAI Micro-Kernel Quantization (u8s8 / fp16)",
        "document": "Arm KleidiAI provides optimized GEMM micro-kernels for LLM inference on Cortex-A and Neoverse cores. The 'u8s8' quantized kernel uses SVE2 dot-product primitives (SDOT/UDOT) delivering 4x throughput over FP32 baseline with <0.2% perplexity degradation.",
        "category": "AI Acceleration",
        "vector_embedding": [0.89, 0.22, 0.88, 0.55, 0.31]
    }
]


def mock_text_embedding(text: str) -> list[float]:
    """Simple deterministic mock text-to-vector embedding function."""
    text_lower = text.lower()
    v1 = 0.9 if "sve" in text_lower or "vector" in text_lower or "gemm" in text_lower else 0.2
    v2 = 0.9 if "errata" in text_lower or "bug" in text_lower or "stall" in text_lower else 0.2
    v3 = 0.9 if "neoverse" in text_lower or "graviton" in text_lower or "trm" in text_lower else 0.2
    v4 = 0.9 if "kleidiai" in text_lower or "quant" in text_lower or "torch" in text_lower else 0.2
    v5 = 0.9 if "numa" in text_lower or "k8s" in text_lower or "memory" in text_lower else 0.2
    return [v1, v2, v3, v4, v5]


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Calculates cosine similarity between two vector embeddings."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0.0


@mcp.tool()
def query_arm_hardware_rag(query_text: str, top_k: int = 2) -> str:
    """Queries the Arm Hardware Knowledge Base Vector DB to retrieve Technical Reference Manuals (TRMs), SVE2 guidelines, and Silicon Errata."""
    query_vec = mock_text_embedding(query_text)
    
    scored_results = []
    for item in ARM_KNOWLEDGE_BASE:
        sim = cosine_similarity(query_vec, item["vector_embedding"])
        scored_results.append({
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "document": item["document"],
            "similarity_score": round(sim, 4)
        })

    scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_results = scored_results[:top_k]

    output = {
        "query": query_text,
        "results_returned": len(top_results),
        "vector_search_results": top_results
    }
    return json.dumps(output, indent=2)


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "SVE2 FMMLA latency on Neoverse"
    print(query_arm_hardware_rag(query))
