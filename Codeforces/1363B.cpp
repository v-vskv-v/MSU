#include <iostream>
#include <string>

uint64_t count01(const std::string &s, size_t pos, uint64_t c)
{
    if (pos == s.size()) {
        return c;
    }
    if (s[pos] == '0') {
        return count01(s, pos + 1, c + 1);
    } else {
        return count01(s, pos + 1, c);
    }
}

uint64_t count10(const std::string &s, size_t pos, uint64_t c)
{
    if (pos == s.size()) {
        return c;
    }
    if (s[pos] == '0') {
        return count10(s, pos + 1, c);
    } else {
        return count10(s, pos + 1, c + 1);
    }
}


uint64_t count0(const std::string &s, size_t pos, uint64_t c)
{
    if (pos == s.size()) {
        return c;
    }
    if (s[pos] == '0') {
        return std::min(count0(s, pos + 1, c), count01(s, pos + 1, c + 1));
    } else {
        return std::min(count0(s, pos + 1, c + 1), count01(s, pos + 1, c));
    }
}

uint64_t count1(const std::string &s, size_t pos, uint64_t c)
{
    if (pos == s.size()) {
        return c;
    }
    if (s[pos] == '0') {
        return std::min(count1(s, pos + 1, c + 1), count10(s, pos + 1, c));
    } else {
        return std::min(count1(s, pos + 1, c), count10(s, pos + 1, c + 1));
    }
}

int main()
{
    int t;
    std::cin >> t;
    while (t--) {
        std::string s;
        std::cin >> s;
        std::cout << std::min(count0(s, 0, 0), count1(s, 0, 0)) << std::endl;
    }
    return 0;
}
