"""
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
https://leetcode.cn/problems/letter-combinations-of-a-phone-number
map = {
    2: "abc",
    3: "def",
    4: "ghi",
    5: "jkl",
    6: "mno",
    7: "pqrs",
    8: "tuv",
    9: "wxyz",
}
"""
from leetcode.basetype import *


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if len(digits) <= 1:
            return self.get_digit_nums(digits)
        ret = list()
        for i in self.get_digit_nums(digits[0]):
            ret.extend([i+j for j in self.letterCombinations(digits[1:])])
        return ret

    def get_digit_nums(self, digit) -> List[str]:
        map = {'2': ['a', 'b', 'c'], '3': ['d', 'e', 'f'], '4': ['g', 'h', 'i'], '5': ['j', 'k', 'l'],
               '6': ['m', 'n', 'o'], '7': ['p', 'q', 'r', 's'], '8': ['t', 'u', 'v'], '9': ['w', 'x', 'y', 'z']}
        return map.get(digit) or list()


if __name__ == '__main__':
    obj = Solution()
    print(obj.letterCombinations("2"))

