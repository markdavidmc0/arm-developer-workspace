#include <vector>
#include <cstdint>
#include <iostream>
#include <chrono>

// Naive quantized depthwise 2D convolution for edge/mobile vision pipelines (MediaPipe target)
void depthwise_conv2d_quantized(const uint8_t* input, const int8_t* kernel, int32_t* output, 
                                int height, int width, int channels, int k_size) {
    int pad = k_size / 2;
    for (int c = 0; c < channels; ++c) {
        for (int h = pad; h < height - pad; ++h) {
            for (int w = pad; w < width - pad; ++w) {
                int32_t sum = 0;
                for (int kh = 0; kh < k_size; ++kh) {
                    for (int kw = 0; kw < k_size; ++kw) {
                        int ih = h + kh - pad;
                        int iw = w + kw - pad;
                        uint8_t pixel = input[(ih * width + iw) * channels + c];
                        int8_t weight = kernel[(kh * k_size + kw) * channels + c];
                        sum += static_cast<int32_t>(pixel) * static_cast<int32_t>(weight);
                    }
                }
                output[(h * width + w) * channels + c] = sum;
            }
        }
    }
}

int main() {
    const int H = 224, W = 224, C = 3, K = 3; // Standard MobileNet resolution
    std::vector<uint8_t> input(H * W * C, 150);
    std::vector<int8_t> kernel(K * K * C, 2);
    std::vector<int32_t> output(H * W * C, 0);

    auto start = std::chrono::high_resolution_clock::now();
    depthwise_conv2d_quantized(input.data(), kernel.data(), output.data(), H, W, C, K);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Quantized Depthwise Conv2D finished in: " << duration.count() << " ms" << std::endl;
    return 0;
}
