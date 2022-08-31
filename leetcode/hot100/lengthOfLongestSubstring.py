"""
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        none_repeat_set = set()
        longest, right = 0, -1
        for left in range(len(s)):
            if left != 0:
                none_repeat_set.remove(s[left-1])
            while right + 1 < len(s) and s[right+1] not in none_repeat_set:
                right += 1
                none_repeat_set.add(s[right])
            longest = max(longest, len(none_repeat_set))
        return longest


if __name__ == '__main__':
    obj = Solution()
    print(obj.lengthOfLongestSubstring("abcabcbb"))
    print(obj.lengthOfLongestSubstring("bbbbb"))
    print(obj.lengthOfLongestSubstring("pwwkew"))
