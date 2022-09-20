"""
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
https://leetcode.cn/problems/kth-largest-element-in-an-array/
"""
from leetcode.basetype import *


class HeapM(object):
    def __init__(self, init: Optional[list] = None):
        if init:
            self._elements = init
            for i in range(len(init)):
                self._siftup(i)
        else:
            self._elements = []  # 初始化堆

    @property
    def heap_len(self) -> int:
        return len(self._elements)

    def get_parent_index(self, index):  # 返回父节点的下标
        if index == 0 or index > self.heap_len - 1:
            return None
        else:
            return (index - 1) >> 1  # 右移//2, 左移*2

    def get_left_index(self, index):  # 返回左节点下标
        left = index * 2 + 1
        if left > self.heap_len - 1:
            return None
        return left

    def get_right_index(self, index):  # 返回右节点下标
        right = index * 2 + 2
        if right > self.heap_len - 1:
            return None
        return right

    def swap(self, left, right):  # 交换数组中的两个元素
        self._elements[left], self._elements[right] = self._elements[right], self._elements[left]

    def extract(self):
        self._elements[0] = self._elements.pop()  # 末尾移到堆顶
        self._siftdown(0)  # 从上到下维护堆

    def top_value(self):
        return self._elements[0]

    def _siftup(self, index):
        if index is not None and index > 0:
            parent = self.get_parent_index(index)  # 当前索引的父索引
            if parent is not None and self._elements[index] > self._elements[parent]:  # 当前值大于父，需要替换
                self.swap(index, parent)
                self._siftup(parent)  # 加入的值换到了父索引位置，继续向上看是不是比上一层的父更大

    def _siftdown(self, index):
        left = self.get_left_index(index)  # 左子树索引
        right = self.get_right_index(index)  # 右子树索引
        new_index = index  # 用一个新索引，后面观察需不需要换
        if right is not None and right < self.heap_len - 1:  # 有左右子树的情况
            # 当前比左右都大，不用操作
            if not (self._elements[left] <= self._elements[index] and self._elements[right] <= self._elements[index]):
                new_index = left if self._elements[left] >= self._elements[right] else right  # 取大值索引
        elif left is not None and left < self.heap_len - 1:  # 只有左子树
            if self._elements[left] >= self._elements[index]:
                new_index = left
        if new_index != index:  # 需要换
            self.swap(new_index, index)
            self._siftdown(new_index)


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = HeapM(nums)
