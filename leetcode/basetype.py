from typing import Optional, List, Set
import random


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @property
    def get_attr(self):
        return ", ".join(f"{k}: {v}" for k, v in self.__dict__.items() if k != "cursor")

    def __str__(self):
        return "{" + self.get_attr + "}"


def new_list_node(l_data: list):
    ret = None
    cursor = None
    for i in l_data:
        if cursor is None:
            ret = ListNode(i)
            cursor = ret
        else:
            cursor.next = ListNode(i)
            cursor = cursor.next
    return ret


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

    def add(self, value):
        self._elements.append(value)  # 放到末尾
        self._siftup(self.heap_len - 1)  # siftup将当前索引值维护到堆的位置

    def extract(self):
        if self.heap_len <= 0:
            raise Exception('empty')
        value = self._elements[0]  # 记录堆顶值
        self._elements[0] = self._elements.pop()  # 末尾移到堆顶
        self._siftdown(0)  # 从上到下维护堆
        return value

    def replace_top(self, val: int):
        if val < self._elements[0]:
            self._elements[0] = val  # 替换堆顶
            self._siftdown(0)  # 从上到下维护堆

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
            # 当前比左右都大
            if not (self._elements[left] <= self._elements[index] and self._elements[right] <= self._elements[index]):
                new_index = left if self._elements[left] >= self._elements[right] else right  # 取大值索引
        elif left is not None and left < self.heap_len - 1:  # 只有左子树
            if self._elements[left] >= self._elements[index]:
                new_index = left
        if new_index != index:  # 需要换
            self.swap(new_index, index)
            self._siftdown(new_index)

    def heapify(self, l: list):
        ...


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


if __name__ == '__main__':
    class Solution:
        def isIdealPermutation(self, nums: List[int]) -> bool:
            glob = part = 0
            for i, v in enumerate(nums):
                if i + 1 <= len(nums) - 1 and nums[i+1] < v:
                    part += 1
                min_v = min(nums[i:])
                if v > min_v:
                    glob += v - min_v
            return glob == part


    obj = Solution()
    import random
    l = list(range(1000))
    random.shuffle(l)
    print(obj.isIdealPermutation(l))
