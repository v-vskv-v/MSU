#include <iostream>
#include <vector>

struct El
{
    bool agr{};
    int val{};
};

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        int n, m;
        std::cin >> n >> m;
        std::vector<std::vector<El>> v;
        v.reserve(n);
        for (int i = 0; i < n; ++i) {
            std::vector<El> vv(m);
            v.push_back(vv);
        }
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                int x;
                std::cin >> x;
                if (x == 1) {
                    for (int k = 0; k < m; k++) {
                        v[i][k].agr = true;
                        v[i][k].val = 1;
                    }
                    for (int k = 0; k < n; k++) {
                        v[k][j].agr = true;
                        v[k][j].val = 1;
                    }
                }
            }
        }
        size_t count1{};
        size_t count2{};
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                if (v[i][j].val == 0) {
                    ++count1;
                    break;
                }
            }
        }
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (v[j][i].val == 0) {
                    ++count2;
                    break;
                }
            }
        }
        if ((std::min(count1, count2) & 1) == 0) {
            std::cout << "Vivek\n";
        } else {
            std::cout << "Ashish\n";
        }
    }
    return 0;
}
