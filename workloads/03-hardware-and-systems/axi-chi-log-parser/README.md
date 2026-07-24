# Workload 08: Simulation Bus Tracker Parser (Design Verification)

This workload parses AXI/CHI simulator logs to match `TX_START` transactions to `TX_END` states and isolate pending protocol hangs, simulating everyday bottlenecks for Arm Design Verification (DV) engineers.

### 💡 Suggested Prompts for IDE Chat:
- *"Analyze `log_parser.cpp` and speed up string scanning using SSE/NEON-based character vector find routines (e.g. `vld1q_u8`)."*
- *"Refactor the active transaction matching vector lookup with a fast hashed structure to eliminate the sequential linear searches."*
