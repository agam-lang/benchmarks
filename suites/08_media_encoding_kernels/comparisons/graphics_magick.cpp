#include <iostream>
#include <vector>

int64_t graphics_magick_filter(int64_t dim) {
    int64_t checksum = 0;
    for (int64_t y = 1; y < dim - 1; ++y) {
        for (int64_t x = 1; x < dim - 1; ++x) {
            int64_t center = (x * y * 31) % 256;
            int64_t top = (x * (y - 1) * 31) % 256;
            int64_t bottom = (x * (y + 1) * 31) % 256;
            int64_t left = ((x - 1) * y * 31) % 256;
            int64_t right = ((x + 1) * y * 31) % 256;
            int64_t laplacian = center * 4 - top - bottom - left - right;
            if (laplacian < 0) laplacian = -laplacian;
            checksum = (checksum + laplacian) % 1000000007;
        }
    }
    return checksum;
}

int main() {
    int64_t res = graphics_magick_filter(512);
    std::cout << res << std::endl;
    return 0;
}
