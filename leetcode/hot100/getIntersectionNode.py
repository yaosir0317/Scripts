"""
给你两个单链表的头节点 headA 和 headB ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 null 。
https://leetcode.cn/problems/intersection-of-two-linked-lists/
"""
from leetcode.basetype import *


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        cursor_a = headA
        cursor_b = headB
        while cursor_a != cursor_b:
            cursor_a = cursor_a.next if cursor_a else headB
            cursor_b = cursor_b.next if cursor_b else headA
        return cursor_a