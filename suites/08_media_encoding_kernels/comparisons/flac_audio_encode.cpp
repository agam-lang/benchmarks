#include <iostream>
#include <vector>

int64_t flac_lpc_encode(int64_t samples) {
    int64_t residual_sum = 0;
    int64_t prev = 0;
    for (int64_t i = 0; i < samples; ++i) {
        int64_t sample = (i * 1103515245 + 12345) % 32768;
        int64_t predicted = prev;
        int64_t residual = sample - predicted;
        if (residual < 0) residual = -residual;
        residual_sum = (residual_sum + residual) % 1000000007;
        prev = sample;
    }
    return residual_sum;
}

int main() {
    int64_t res = flac_lpc_encode(100000);
    std::cout << res << std::endl;
    return 0;
}
