#include <iostream>
#include <vector>
#include <cstdint>

int main()
{
    int t, n, x;
    std::cin >> t;
    while (t--) {
        int64_t count[2] = {0, 0};
        std::cin >> n >> x;
        for (int i = 0; i < n; ++i) {
            int p;
            std::cin >> p;
            count[p % 2]++;
        }
        if (count[1] == 0) {
            std::cout << "No\n";
        } else {
            x--;
            count[1]--;
            x -= (count[1] >> 1) << 1;
            if (x < 0) {
                if ((x & 1) == 0 || count[0] > 0) {
                    std::cout << "Yes\n";
                } else  {
                    std::cout << "No\n";
                }
            } else if (x <= count[0]) {
                std::cout << "Yes\n";
            } else {
                std::cout << "No\n";
            }
        }
    }
    return 0;
}
