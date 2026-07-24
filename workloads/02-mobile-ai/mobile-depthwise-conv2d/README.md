# Workload 06: Client-Side Mobile Vision (Quantized Depthwise Conv2D)

This workload represents real-time video filtering and classification tasks running locally on mobile CPUs or Edge NPUs under tight battery and heat dissipation budgets.

### 💡 Suggested Prompts for IDE Chat:
- *"Examine `depthwise_conv2d.cpp` and rewrite it using Arm SME2 matrix tile instructions to maximize mobile GPU/CPU coprocessor offloading."*
- *"Dispatch this loop to KleidiAI / XNNPACK optimized depthwise kernels and benchmark the output latency changes."*
