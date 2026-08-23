#include <iostream>
#include <vector>

int64_t c_ray_4k_trace(int64_t width, int64_t height, int64_t spp) {
    int64_t hits = 0;
    int64_t sphere_radius_sq = 250000;
    for (int64_t y = 0; y < height; ++y) {
        for (int64_t x = 0; x < width; ++x) {
            for (int64_t s = 0; s < spp; ++s) {
                int64_t rx = x - width / 2;
                int64_t ry = y - height / 2;
                int64_t dist_sq = rx * rx + ry * ry;
                if (dist_sq <= sphere_radius_sq) {
                    hits++;
                }
            }
        }
    }
    return hits;
}

int main() {
    int64_t res = c_ray_4k_trace(256, 256, 16);
    std::cout << res << std::endl;
    return 0;
}
