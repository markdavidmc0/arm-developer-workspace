# Workload 07: Set-Associative Cache Simulator (HW Modeling)

This workload models L1/L2 cache sets, tags, and Least Recently Used (LRU) line evictions, simulating core bottlenecks encountered by Arm Architectural & SystemC Simulation Modeling engineers.

### 💡 Suggested Prompts for IDE Chat:
- *"Analyze `cache_sim.cpp` and optimize the associativity loop scan by storing line states in a single compact bit-vector."*
- *"Refactor the LRU lookup routines to run parallel checks on the sets using vector registers to speed up the simulation runtime."*
