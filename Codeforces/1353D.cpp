#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

struct Cmp
{
	bool operator() (const std::pair<size_t, size_t> &a,
	        const std::pair<size_t, size_t> &b) const {
		int size_a = a.second - a.first;
		int size_b = b.second - b.first;
		if (size_a == size_b) {
		    return a.first < b.first;
		}
		return size_a > size_b;
	}
};

int main()
{
    size_t n;
    size_t j;
    std::cin >> j;
    while (j--) {
        std::cin >> n;
        std::vector<size_t> v(n);
        std::set<std::pair<size_t, size_t>, Cmp> w{{0, n - 1}};
        for (size_t i = 1; i <= n; ++i) {
            auto [l, r] = *w.begin();
            w.erase(w.begin());
            size_t t = (l + r) >> 1;
            v[t] = i;
            if (t > l) {
                w.emplace(std::pair<size_t, size_t>(l, t - 1));
            }
            if (r > t) {
                w.emplace(std::pair<size_t, size_t>(t + 1, r));
            }
        }
        for (auto &c : v) {
            std::cout << c << ' ';
        }
        std::cout << std::endl;
    }
    return 0;
}
