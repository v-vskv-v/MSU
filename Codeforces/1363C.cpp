#include <iostream>
#include <vector>
#include <map>
#include <string>

int main()
{
    int t;
    std::map<int, std::string> ans{{0, "Ayush"}, {1, "Ashish"}};
    std::cin >> t;
    while (t--) {
        int x, n;
        int st = 0;
        std::cin >> n >> x;
        std::vector<std::vector<bool>> graph(n);
        for (int i = 0; i < n; ++i) {
            graph[i].reserve(n);
        }
        for (int i = 1; i < n; ++i) {
            int u, v;
            std::cin >> u >> v;
            graph[u - 1][v - 1] = graph[v - 1][u - 1] = true;
        }
        if (n < 3) {
            std::cout << ans[st] << std::endl;
        } else {
            int sum{};
            for (int j = 0; j < n; ++j) {
                sum += graph[x - 1][j];
            }
            if (sum == 1) {
                std::cout << ans[st] << std::endl;
            } else {
                int steps = n - 3;
                st = steps & 1;
                std::cout << ans[(st + 1) % 2] << std::endl;
            }
        }
    }
    return 0;
}
