#include <iostream>
#include <cstdint>
#include <vector>

enum { N = 1000000007 };

int64_t pow(int64_t a, int64_t b)
{
    int64_t p = 1;
    while (b) {
        if (b & 1) {
            p = (p * a) % N;
        }
        b >>= 1;
        a = (a * a) % N;
    }
    return p;
}

int64_t dfs(std::vector<bool> &visited, const std::vector<std::vector<int64_t>> &info, int64_t i)
{
    int64_t sz{};
	if (!visited[i]) {
	    visited[i] = true;
	    sz++;
        for (auto &n: info[i]) {
            sz += dfs(visited, info, n);
	    }
    }
	return sz;
}

int main()
{
    int64_t n, k;
    int64_t u, v, x;
    std::cin >> n >> k;
    std::vector<std::vector<int64_t>> info(n);
    int64_t ans = pow(n, k);
    for (int64_t i = 1; i < n; ++i) {
        std::cin >> u >> v >> x;
        if (x == 0) {
            info[u - 1].push_back(v - 1);
            info[v - 1].push_back(u - 1);
        }
    }
    std::vector<bool> visited(n);
    for (int64_t i = 0; i < n; ++i) {
        if (!visited[i]) {
            ans -= pow(dfs(visited, info, i), k);
            ans += N;
            ans %= N;
        }
    }
    std::cout << ans << std::endl;  
    return 0;
}
