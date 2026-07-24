#include <vector>
#include <iostream>
#include <chrono>

// Boilerplate Naive Baseline Kernel (Replace with your own workload algorithm)
void naive_baseline_kernel(const float* input, float* output, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        // Naive unoptimized operation (Target for Arm SIMD/NEON/SVE or library optimization)
        output[i] = input[i] * 2.0f; 
    }
}

int main() {
    const size_t SIZE = 1048576; // 1M elements
    std::vector<float> input(SIZE, 1.0f);
    std::vector<float> output(SIZE, 0.0f);

    auto start = std::chrono::high_resolution_clock::now();
    naive_baseline_kernel(input.data(), output.data(), SIZE);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Baseline kernel finished execution in: " << duration.count() << " ms" << std::endl;
    return 0;
}
