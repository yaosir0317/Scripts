"""
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。
找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。
返回容器可以储存的最大水量。
说明：你不能倾斜容器。
https://leetcode.cn/problems/container-with-most-water/
"""
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxArea = (len(height) - 1) * min(height[0], height[-1])
        left, right = 0, len(height) - 1
        while left < right:
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1
            maxArea = max(maxArea, (right - left) * min(height[left], height[right]))
        return maxArea


if __name__ == '__main__':
    obj = Solution()
    print(obj.maxArea([1,1]))
