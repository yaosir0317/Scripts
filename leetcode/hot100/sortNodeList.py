"""
给你链表的头结点 head ，请将其按 升序 排列并返回 排序后的链表 。
https://leetcode.cn/problems/sort-list/
"""

from leetcode.basetype import *


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        left, right = self.splitListMid(head)
        return self.mergeList(self.sortList(left), self.sortList(right))

    def splitListMid(self, head: Optional[ListNode]) -> (Optional[ListNode], Optional[ListNode]):
        mock = ListNode(val=0, next=head)
        slow = mock
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        ret = slow.next
        slow.next = None
        return head, ret

    def mergeList(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if not l1:
            return l2
        if not l2:
            return l1
        if l1.val > l2.val:
            return ListNode(val=l2.val, next=self.mergeList(l1, l2.next))
        else:
            return ListNode(val=l1.val, next=self.mergeList(l1.next, l2))


if __name__ == '__main__':
    ...