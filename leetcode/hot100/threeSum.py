"""
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请

你返回所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。
https://leetcode.cn/problems/3sum/
"""
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        for cursor, value in enumerate(nums):
            sub = self.exists_two_num(value, nums, cursor)
            for i in sub:
                if cursor != i[0] != i[1]:
                    print(cursor, i)
                    result.append([nums[cursor], nums[i[0]], nums[i[1]]])
        return result

    def exists_two_num(self, val: int, nums: List[int], cursor: int):
        val = -val
        d = dict()
        ret = list()
        for index, v in enumerate(nums[cursor:], start=cursor):
            find = val - v
            if find in d:
                ret.append([d[find], index])
            d[v] = index
        return ret


if __name__ == '__main__':
    ...
