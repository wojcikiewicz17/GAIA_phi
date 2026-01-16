#include "../headers/omega_protocol.h"
omega_float recursive_resonance(omega_float* input, omega_float* memory, int n) {
    return (n <= 0) ? 0.0f : (*input * *memory) + recursive_resonance(input + 1, memory + 1, n - 1);
}
