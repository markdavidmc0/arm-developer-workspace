# Workload 05: Audio Pipeline mel Preprocessing (Whisper Target)

This workload focuses on pre-spectrogram floating-point sliding frames common in scalable cloud audio translation APIs (e.g. Whisper, Speech-to-Text).

### 💡 Suggested Prompts for IDE Chat:
- *"Optimize `mel_framing.cpp` using compiler flags targeting Google Axion processors (e.g., `-march=armv9-a+sve2`)."*
- *"Provide a hand-coded SVE implementation of `apply_hamming_window` to maximize L1/L2 cache locality and pipeline utilization on Neoverse cores."*
