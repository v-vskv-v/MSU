#include <iostream>
#include <vector>
#include <algorithm>

struct El
{
    int a{};
    int b{};
};

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        int n;
        bool if_0{};
        bool if_1{};
        std::cin >> n;
        std::vector<int> v(n);
        for (int i = 0; i < n; ++i) {
            std::cin >> v[i];
        }
        for (int i = 0; i < n; ++i) {
            int x;
            std::cin >> x;
            if (x == 0 && !if_0) {
                if_0 = true;
            } else if (x == 1 && !if_1) {
                if_1 = true;
            }
        }
        bool fl = true;
        if (!if_0 || !if_1) {
            for (int i = 1; i < v.size(); ++i) {
                if (v[i] < v[i - 1]) {
                    fl = false;
                    break;
                }
            }
        }
        if (fl) {
            std::cout << "Yes\n";
        } else {
            std::cout << "No\n";
        }
    }
    return 0;
}
