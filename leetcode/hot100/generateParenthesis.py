from leetcode.basetype import *


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if n == 1:
            return ["()"]
        res = set()
        for i in self.generateParenthesis(n - 1):
            for j in range(len(i)):
                res.add(i[0:j] + '()' + i[j:])
        return list(res)


if __name__ == '__main__':
    obj = Solution()
    print(obj.generateParenthesis(4))
