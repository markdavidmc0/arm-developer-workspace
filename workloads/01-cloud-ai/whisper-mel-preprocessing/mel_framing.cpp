#include <vector>
#include <cmath>
#include <iostream>
#include <chrono>

// Naive Sliding-Window framing and Window multiplication (Whisper Audio Pipeline Target)
void apply_hamming_window(const float* signal, const float* window, float* output, int frame_size, int num_frames) {
    for (int f = 0; f < num_frames; ++f) {
        for (int i = 0; i < frame_size; ++i) {
            output[f * frame_size + i] = signal[f * frame_size + i] * window[i];
        }
    }
}

int main() {
    const int FRAME_SIZE = 400; // 25ms framing window at 16kHz audio sampling rate
    const int NUM_FRAMES = 10000;
    
    std::vector<float> signal(NUM_FRAMES * FRAME_SIZE, 0.35f);
    std::vector<float> window(FRAME_SIZE, 0.54f);
    std::vector<float> output(NUM_FRAMES * FRAME_SIZE, 0.0f);

    auto start = std::chrono::high_resolution_clock::now();
    apply_hamming_window(signal.data(), window.data(), output.data(), FRAME_SIZE, NUM_FRAMES);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Audio framing preprocessing finished in: " << duration.count() << " ms" << std::endl;
    return 0;
}
