#include <vector>
#include <cmath>
#include <iostream>

// Naive SiLU Activation (Target for ExecuTorch / Arm Compute Library Integration)
void silu_activation(const float* input, float* output, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        float x = input[i];
        output[i] = x / (1.0f + std::exp(-x));
    }
}

int main() {
    const size_t SIZE = 1024 * 1024;
    std::vector<float> in(SIZE, 0.5f);
    std::vector<float> out(SIZE, 0.0f);

    silu_activation(in.data(), out.data(), SIZE);
    std::cout << "SiLU Activation evaluated over " << SIZE << " elements." << std::endl;
    return 0;
}
