# 🤝 Contributing Workloads to Arm AI Workspace

Welcome! Help us expand the benchmark suite by contributing your Arm optimization workloads (C++, Neon, KleidiAI, ExecuTorch, OpenCV, or llama.cpp operators).

## 🚀 How to Add a Use Case:
1. Identify the core priority area for your workload:
   - `workloads/00-foundations/` (Numeric kernels & general vectorization)
   - `workloads/01-cloud-ai/` (Large models, server optimizations, DB, and API pipelines)
   - `workloads/02-mobile-ai/` (Edge/On-device optimizations, battery constraints, app runtimes)
   - `workloads/03-hardware-and-systems/` (Silicon modeling, page walker simulations, and log parsers)
   - `workloads/04-physical-ai/` (Real-world robotics perception, sensor streams, and controls)

2. Copy the template folder into your target priority directory:
   `cp -r workloads/_template workloads/[priority-category]/your-usecase-name`

3. Add your baseline unoptimized code to `kernel.cpp` (or standard C++ source files).

4. Update the local `README.md` inside your new workload folder with 2-3 targeted chat agent prompts.

5. Add your workload to the main catalog in the root `README.md` and open a Pull Request (PR) to this repository!

> 💬 Need assistance or running into issues? Ping us in the Hackathon Discord!
