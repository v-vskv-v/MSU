#include <iostream>
#include <cstdint>

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        uint64_t n, m, a;
        std::cin >> n >> m >> a;
        uint64_t s{};
        uint64_t num;
        for (size_t i = 1; i < n; ++i) {
            std::cin >> num;
            s += num;
        }
        if (s + a > m) {
            a = m;
        } else {
            a += s;
        }
        std::cout << a << std::endl;
    }
    return 0;
}
