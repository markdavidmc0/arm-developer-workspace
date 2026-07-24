# Workload 01: C++ SIMD & Arm NEON Vectorization

This workload demonstrates auto-vectorization and hand-crafted Arm NEON SIMD transformation for C++ numeric computing.

### 💡 Suggested Prompts for IDE Chat:
- *"Profile `matrix_mul.cpp` on the remote Arm Tau T2A sandbox and identify loop bottlenecks."*
- *"Refactor `naive_matrix_multiply` using 128-bit Arm NEON intrinsics (`vld1q_f32`, `vmlaq_f32`) and benchmark the speedup."*
