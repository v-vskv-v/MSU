#include <iostream>
#include <vector>
#include <string>
#include <queue>

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        int n, m;
        std::cin >> n >> m;
        std::vector<std::string> v(n);
        for (int i = 0; i < n; ++i) {
            std::cin >> v[i];
        }
        
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                if (v[i][j] == 'B') {
                    if (i > 0 && v[i - 1][j] == '.') {
                        v[i - 1][j] = '#';
                    }
                    if (i + 1 < n && v[i + 1][j] == '.') {
                        v[i + 1][j] = '#';
                    }
                    if (j > 0 && v[i][j - 1] == '.') {
                        v[i][j - 1] = '#';
                    }
                    if (j + 1 < m && v[i][j + 1] == '.') {
                        v[i][j + 1] = '#';
                    }
                }
            }
        }
        std::vector<std::vector<bool>> visited;
        for (int i = 0; i < n; ++i) {
            visited.push_back(std::vector<bool>(m));
        }
        std::queue<std::pair<int, int>> q;
        if (v[n - 1][m - 1] == '.') {
            q.push({n - 1, m - 1});
            visited[n - 1][m - 1] = true;
        }
        while (!q.empty()) {
            auto [i, j] = q.front();            
            q.pop();
            if (i > 0 && !visited[i - 1][j] && v[i - 1][j] != '#') {
                q.push({i - 1, j});
                visited[i - 1][j] = true;
            }
            if (i + 1 < n && !visited[i + 1][j] && v[i + 1][j] != '#') {
                q.push({i + 1, j});
                visited[i + 1][j] = true;
            }
            if (j > 0 && !visited[i][j - 1] && v[i][j - 1] != '#') {
                q.push({i, j - 1});
                visited[i][j - 1] = true;
            }
            if (j + 1 < m && !visited[i][j + 1] && v[i][j + 1] != '#') {
                q.push({i, j + 1});
                visited[i][j + 1] = true;
            } 
        }

        bool flag = true;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                if ((v[i][j] == 'G' && !visited[i][j]) || (v[i][j] == 'B' && visited[i][j])) {
                    flag = false;
                    break;
                }
            }
            if (!flag) {
                break;
            }
        }
        if (flag) {
            std::cout << "Yes" << std::endl;
        } else {
            std::cout << "No" << std::endl;
        }
    }
    return 0;
}
