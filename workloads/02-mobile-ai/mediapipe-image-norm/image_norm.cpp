#include <vector>
#include <cstdint>
#include <iostream>

// Baseline RGB24 to Float Tensor Normalization (Camera preprocessing for mobile AI)
void normalize_rgb(const uint8_t* rgb_in, float* tensor_out, size_t num_pixels) {
    for (size_t i = 0; i < num_pixels * 3; ++i) {
        tensor_out[i] = (static_cast<float>(rgb_in[i]) / 127.5f) - 1.0f;
    }
}

int main() {
    const size_t pixels = 1920 * 1080;
    std::vector<uint8_t> raw_rgb(pixels * 3, 128);
    std::vector<float> tensor(pixels * 3, 0.0f);
    normalize_rgb(raw_rgb.data(), tensor.data(), pixels);
    std::cout << "Normalized 1080p frame tensor successfully." << std::endl;
    return 0;
}
