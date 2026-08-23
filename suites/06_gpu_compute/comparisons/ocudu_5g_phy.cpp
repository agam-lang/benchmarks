#include <iostream>
#include <vector>

int64_t ocudu_ldpc_decode(int64_t num_blocks, int64_t block_size) {
    int64_t corrected_parity = 0;
    for (int64_t b = 0; b < num_blocks; ++b) {
        int64_t syndrome = 0;
        for (int64_t i = 0; i < block_size; ++i) {
            int64_t llr = ((b * 31 + i * 17) % 256) - 128;
            if (llr < 0) {
                syndrome = (syndrome + 1) % 2;
            }
        }
        corrected_parity = (corrected_parity * 31 + syndrome) % 1000000007;
    }
    return corrected_parity;
}

int main() {
    int64_t res = ocudu_ldpc_decode(1000, 64);
    std::cout << res << std::endl;
    return 0;
}
