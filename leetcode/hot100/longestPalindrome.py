"""
给你一个字符串 s，找到 s 中最长的回文子串。
https://leetcode.cn/problems/longest-palindromic-substring/
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:
            return s
        max_left = max_right = 0
        for cursor in range(len(s)-1):
            left_odd, right_odd = self.maxPalindrome(s, cursor, cursor)
            left_even, right_even = self.maxPalindrome(s, cursor, cursor + 1)
            if right_odd - left_odd > max_right - max_left:
                max_left, max_right = left_odd, right_odd
            if right_even - left_even > max_right - max_left:
                max_left, max_right = left_even, right_even
        return s[max_left: max_right+1]

    @staticmethod
    def maxPalindrome(s: str, left: int, right: int):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left+1, right-1


if __name__ == '__main__':
    obj = Solution()
    print(obj.longestPalindrome("ccc"))