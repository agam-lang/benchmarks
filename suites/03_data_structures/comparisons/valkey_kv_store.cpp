#include <iostream>
#include <vector>

int64_t valkey_pipeline(int64_t operations) {
    int64_t checksum = 0;
    int64_t store[1024] = {0};
    for (int64_t i = 0; i < operations; ++i) {
        int64_t slot = (i * 31) % 1024;
        int64_t val = (i * 17 + 101) % 100000;
        store[slot] = val;
        int64_t read_back = store[(slot + 7) % 1024];
        checksum = (checksum + read_back) % 1000000007;
    }
    return checksum;
}

int main() {
    int64_t res = valkey_pipeline(50000);
    std::cout << res << std::endl;
    return 0;
}
