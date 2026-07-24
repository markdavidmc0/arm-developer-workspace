#include <vector>
#include <iostream>
#include <chrono>

// Baseline Naive Kalman Filter State Prediction (Target for NEON / SVE Vectorization)
// Computes: State = Transition * State + Control * ControlInput
void predict_state_naive(float* state, const float* transition, const float* control, const float* control_input, int dims) {
    std::vector<float> next_state(dims, 0.0f);
    for (int i = 0; i < dims; ++i) {
        float sum = 0.0f;
        for (int j = 0; j < dims; ++j) {
            sum += transition[i * dims + j] * state[j];
        }
        sum += control[i] * control_input[i];
        next_state[i] = sum;
    }
    for (int i = 0; i < dims; ++i) {
        state[i] = next_state[i];
    }
}

int main() {
    const int DIMS = 4;
    const int ITERATIONS = 1000000;
    
    // 4D state vector [x, y, dx, dy]
    std::vector<float> state = {0.0f, 0.0f, 1.0f, 1.0f};
    
    // State transition matrix (4x4)
    std::vector<float> transition = {
        1.0f, 0.0f, 0.1f, 0.0f,
        0.0f, 1.0f, 0.0f, 0.1f,
        0.0f, 0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 0.0f, 1.0f
    };
    
    std::vector<float> control = {0.5f, 0.5f, 0.2f, 0.2f};
    std::vector<float> control_input = {0.1f, 0.1f, 0.05f, 0.05f};

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < ITERATIONS; ++i) {
        predict_state_naive(state.data(), transition.data(), control.data(), control_input.data(), DIMS);
    }
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Kalman Filter Predict (" << ITERATIONS << " cycles): " << duration.count() << " ms" << std::endl;
    std::cout << "Final Predicted State Vector: [" << state[0] << ", " << state[1] << "]" << std::endl;
    return 0;
}
