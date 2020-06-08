#include <iostream>
#include <vector>
#include <cstdint>

int main()
{
    size_t n;
    std::cin >> n;
    if (n < 3) {
        std::cout << 0 << std::endl;
    } else {
        std::vector<int64_t> v;
        int64_t s{};
        for (size_t i = 0; i < n; ++i) {
            int64_t l;
            std::cin >> l;
            s += l;
            v.push_back(l);
        }
        if (s % 3 != 0) {
            std::cout << 0 << std::endl;
        } else {
            int64_t ss{};
            uint64_t count{};
            std::vector<uint64_t> cnt(n);
            for (int i = n - 1; i >= 0; --i) {
                ss += v[i];
                if (ss == s / 3) {
                    ++count;
                }
                cnt[i] = count;
            }
            count = 0;
            ss = 0;
            for (size_t j = 0; j < n - 2; ++j) {
                ss += v[j];
                if (ss == s / 3) {
                    count += cnt[j + 2];
                }
            }
            std::cout << count << std::endl;
        }
    }
    return 0;
}
