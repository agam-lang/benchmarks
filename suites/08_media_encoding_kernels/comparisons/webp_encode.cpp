#include <iostream>
#include <vector>

int64_t paeth_predictor(int64_t a, int64_t b, int64_t c) {
    int64_t p = a + b - c;
    int64_t pa = p > a ? p - a : a - p;
    int64_t pb = p > b ? p - b : b - p;
    int64_t pc = p > c ? p - c : c - p;
    if (pa <= pb && pa <= pc) return a;
    if (pb <= pc) return b;
    return c;
}

int64_t webp_encode(int64_t width, int64_t height) {
    int64_t residual_sum = 0;
    for (int64_t y = 1; y < height; ++y) {
        for (int64_t x = 1; x < width; ++x) {
            int64_t left = ((x - 1) * 17 + y * 23) % 256;
            int64_t top = (x * 17 + (y - 1) * 23) % 256;
            int64_t top_left = ((x - 1) * 17 + (y - 1) * 23) % 256;
            int64_t current = (x * 17 + y * 23) % 256;
            int64_t predicted = paeth_predictor(left, top, top_left);
            int64_t diff = current - predicted;
            if (diff < 0) diff = -diff;
            residual_sum = (residual_sum + diff) % 1000000007;
        }
    }
    return residual_sum;
}

int main() {
    int64_t res = webp_encode(512, 512);
    std::cout << res << std::endl;
    return 0;
}
