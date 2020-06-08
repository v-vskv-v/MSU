#include <iostream>
#include <vector>

int main()
{
    int n;
    std::cin >> n;
    std::vector<size_t> a(n + 1);
    std::vector<size_t> b(n + 1);
    std::vector<size_t> pos(n + 1);
    std::vector<size_t> find_max(n + 1);

    for (int i = 1; i <= n; ++i) {
        std::cin >> a[i];
        pos[a[i]] = i;
    }
    for (int i = 1; i <= n; ++i) {
        std::cin >> b[i];
    }
    for (int i = 1; i <= n; ++i) {
        int k = pos[b[i]] - i;
        if (k < 0) {
            k += n;
        }
        find_max[k]++;
    }
    size_t ans{};
    for (auto &el : find_max) {
        ans = std::max(ans, el);
    }
    std::cout << ans << std::endl;
    return 0;
}
