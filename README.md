# 🦾 Arm AI Developer Workspace

> ℹ️ **Architecture Note:** This repository is the **Developer Client Workspace**. It connects securely to the remote [Arm AI Control Plane](https://github.com/your-org/arm-ai-control-plane) deployed on GCP Tau T2A instances running sandboxed gVisor runtime environments.

---

## ⚡ 30-Second Quickstart for Hackathon Judges & Developers

This workspace requires **zero local build toolchains, Docker, or compiler configuration**.

### Step 1: Open in VS Code or Cursor
Clone and open this folder in Cursor or VS Code:
```bash
git clone https://github.com/your-org/arm-developer-workspace.git
cd arm-developer-workspace
```

### Step 2: Automatic Tool Discovery
Your IDE will automatically detect `.vscode/mcp.json` (and `.cursor/mcp.json`) and connect over HTTPS/SSE to our live GCP Tau T2A Control Plane.

### Step 3: Run Your First Prompt
Open any C++ kernel in `workloads/` (e.g., `workloads/00-foundations/cpp-simd-neon-matmul/matrix_mul.cpp`) and ask your IDE agent:
*"Profile `matrix_mul.cpp` on the remote Arm Tau T2A sandbox, optimize it with 128-bit Arm NEON intrinsics, and benchmark the execution time diff."*

## 📂 Workload & Persona Catalog

| Category | Workload Folder | Description | Primary Target / Persona |
| :--- | :--- | :--- | :--- |
| **00-Foundations** | [`cpp-simd-neon-matmul`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/00-foundations/cpp-simd-neon-matmul/) | Naive scalar matrix multiplication | Numeric & Low-Level Engineers |
| **01-Cloud AI** | [`llamacpp-int4-dequant`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/01-cloud-ai/llamacpp-int4-dequant/) | LLM INT4 Weight Unpacking & GEMM loop | LLM Core & Cloud Infrastructure Eng |
| **01-Cloud AI** | [`kleidiai-gemm-u8s8`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/01-cloud-ai/kleidiai-gemm-u8s8/) | Quantized GEMM micro-kernel fallbacks | ML Platform & LLM Engine Teams |
| **01-Cloud AI** | [`whisper-mel-preprocessing`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/01-cloud-ai/whisper-mel-preprocessing/) | Audio Spectrogram Framing & windowing | Audio ML & Preprocessing Pipeline Eng |
| **02-Mobile AI** | [`mediapipe-image-norm`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/02-mobile-ai/mediapipe-image-norm/) | Camera RGB24 to Float Tensor Normalization | On-Device AI / MediaPipe App Devs |
| **02-Mobile AI** | [`executorch-silu-op`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/02-mobile-ai/executorch-silu-op/) | Naive custom SiLU activation operator | On-Device / ExecuTorch Integration Devs |
| **02-Mobile AI** | [`mobile-depthwise-conv2d`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/02-mobile-ai/mobile-depthwise-conv2d/) | Quantized Depthwise separable 2D Convolution | Client App / Mobile Vision Engineers |
| **03-Hardware & Systems** | [`tlb-page-table-walker`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/03-hardware-and-systems/tlb-page-table-walker/) | MMU Page Table translation walker simulation | Architectural Modeling & SystemC Eng |
| **03-Hardware & Systems** | [`cache-associativity-sim`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/03-hardware-and-systems/cache-associativity-sim/) | L1/L2 Set-Associative Cache simulator | Processor Architecture & gem5 Modeling Eng |
| **03-Hardware & Systems** | [`axi-chi-log-parser`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/03-hardware-and-systems/axi-chi-log-parser/) | Bus Handshake protocol violation analyzer | Design Verification (DV) / RTL Eng |
| **04-Physical AI** | [`ros2-pointcloud-voxel`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/04-physical-ai/ros2-pointcloud-voxel/) | LiDAR 3D PointCloud voxel grid spatial filtering | Robotics / Autonomous Perception Devs |
| **04-Physical AI** | [`sensor-fusion-kalman`](file:///Users/markmcnaught/Repos/arm-developer-workspace/workloads/04-physical-ai/sensor-fusion-kalman/) | Kalman Filter multi-dimensional state predict | Autonomous Navigation & Controls Eng |

## 🤝 Contributing New Workloads

Have a custom C++ benchmark or model operator? Read our [CONTRIBUTING.md](file:///Users/markmcnaught/Repos/arm-developer-workspace/CONTRIBUTING.md) guide to add your workload in under 2 minutes!
