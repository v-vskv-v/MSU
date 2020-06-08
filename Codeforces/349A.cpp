#include <iostream>

enum { N = 25 };

int main()
{
    size_t n;
    size_t k;
    size_t i{};
    std::cin >> n;
    int nums[3] = {0};
    for (; i < n; ++i) {
        std::cin >> k;
        ++nums[k / N - 1];
        if (k > N) {
            k -= N;
            if (k == 3 * N) {
                if (nums[1]) {
                    --nums[1];
                    k -= 2 * N;
                    if (!nums[0]--) {
                        break;
                    }
                } else if ((nums[0] -= 3) < 0) {
                    break;
                }
            } else if (k == N && !nums[0]--) {
                break;
            }
        }
    }
    if (i == n) {
        std::cout << "YES" << std::endl;
    } else {
        std::cout << "NO" << std::endl;
    }
    return 0;
}
