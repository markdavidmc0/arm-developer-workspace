#include <vector>
#include <cstdint>
#include <iostream>

// Baseline INT4 Weight Unpacking + FP16/FP32 GEMM (Core bottleneck in llama.cpp / vLLM)
void int4_dequant_gemm(const uint8_t* packed_weights, const float* x, float* y, int K, int N) {
    for (int n = 0; n < N; ++n) {
        float sum = 0.0f;
        for (int k = 0; k < K; k += 2) {
            uint8_t packed = packed_weights[(n * K + k) / 2];
            int8_t w0 = (packed & 0x0F) - 8;
            int8_t w1 = ((packed >> 4) & 0x0F) - 8;
            sum += static_cast<float>(w0) * x[k];
            sum += static_cast<float>(w1) * x[k + 1];
        }
        y[n] = sum;
    }
}

int main() {
    const int K = 4096, N = 1024;
    std::vector<uint8_t> packed_weights((K * N) / 2, 0x5A);
    std::vector<float> x(K, 1.0f), y(N, 0.0f);
    int4_dequant_gemm(packed_weights.data(), x.data(), y.data(), K, N);
    std::cout << "INT4 Dequantization GEMM evaluation complete." << std::endl;
    return 0;
}
