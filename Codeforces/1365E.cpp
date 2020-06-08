#include <iostream>
#include <cstdint>
#include <vector>

int main()
{
    int n;
    std::cin >> n;
    std::vector<uint64_t> v(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> v[i];
    }

    uint64_t ans{};
    for (int k = n - 1; k >= 0; --k) {
        for (int i = k; i >= 0; --i) {
            for (int j = i; j >= 0; --j) {
                ans = std::max(ans, v[k] | v[i] | v[j]);
            }
        }
    }
    std::cout << ans << std::endl;
    return 0;
}
