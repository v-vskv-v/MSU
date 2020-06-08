#include <iostream>
#include <vector>
#include <string>

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        int n, k;
        int full_max, curr;
        std::vector<std::vector<int>> set;
        std::vector<int> set_c;
        std::cin >> n >> k;
        std::vector<int> ans(k);
        for (int i = 0; i < k; ++i) {
            int c;
            std::cin >> c;
            std::vector<int> v(c);
            for (int j = 0; j < c; ++j) {
                std::cin >> v[j];
            }
            set_c.push_back(c);
            set.push_back(v);
        }
        std::cout << "? " << n;
        for (int i = 1; i <= n; ++i) {
            std::cout << ' ' << i;
        }
        std::cout << std::endl;
        std::cin >> full_max;
        int i1 = 0;
        int i2 = k;
        int half = (i1 + i2) >> 1;
        while (i1 != half) {

            int sum{};
            for (int i = i1; i < half; ++i) {
                sum += set_c[i];
            }
            std::cout << "? " << sum;
            for (int i = i1; i < half; ++i) {
                for (auto &r: set[i]) {
                    std::cout << ' ' << r;
                }
            }
            std::cout << std::endl;
            std::cin >> curr;
            if (curr == full_max) {
                i2 = half;
            } else {
                i1 = half;
            }
            half = (i1 + i2) >> 1;
        }

        std::vector<bool> others(n, true);
        for (auto &r : set[i1]) {
            others[r - 1] = false;
        }

        std::cout << "? " << n - set_c[i1];
        for (int i = 0; i < n; ++i) {
            if (others[i]) {
                std::cout << ' ' << i + 1;
            }
        }
        std::cout << std::endl;
        std::cin >> ans[i1];

        for (int i = 0; i < k; ++i) {
            if (i != i1) {
                ans[i] = full_max;
            }
        }

        std::cout << "!";
        for (auto &r : ans) {
            std::cout << ' ' << r;
        }
        std::cout << std::endl;
        std::string line;
        std::cin >> line;
        if (line != "Correct") {
            break;
        }
    }
    return 0;
}
