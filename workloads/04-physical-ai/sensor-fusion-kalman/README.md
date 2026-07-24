# Workload 04: Real-Time Robotics Sensor Fusion (Kalman Filter)

This workload targets high-frequency, low-latency control-loop bottlenecks common in ROS 2, Zenoh, and autonomous driving middleware on edge SoCs.

### 💡 Suggested Prompts for IDE Chat:
- *"Analyze `kalman_filter.cpp` and replace the naive matrix prediction loop with a highly vectorized Arm NEON or SVE version to support high-frequency 1000Hz sensor fusion streams."*
- *"Optimize memory bandwidth by removing the intermediate `next_state` heap-allocated vectors and benchmarking the latency on GCP Tau T2A."*
