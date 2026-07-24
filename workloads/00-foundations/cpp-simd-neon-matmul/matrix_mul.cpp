#include <vector>
#include <iostream>
#include <chrono>

// Baseline Naive Scalar Matrix Multiplication (Target for Arm NEON SIMD Optimization)
void naive_matrix_multiply(const float* A, const float* B, float* C, int N) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            float sum = 0.0f;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}

int main() {
    const int N = 256;
    std::vector<float> A(N * N, 1.5f);
    std::vector<float> B(N * N, 2.0f);
    std::vector<float> C(N * N, 0.0f);

    auto start = std::chrono::high_resolution_clock::now();
    naive_matrix_multiply(A.data(), B.data(), C.data(), N);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Execution Time (Naive Scalar): " << duration.count() << " ms" << std::endl;
    return 0;
}
