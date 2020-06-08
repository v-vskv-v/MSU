#include <iostream>
#include <cstdint>

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        uint64_t n;
        std::cin >> n;
        n >>= 1;
        std::cout << 4 * n * (n + 1) * (2 * n + 1) / 3 << std::endl;
    }
    return 0;
}
