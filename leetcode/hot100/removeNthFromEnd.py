"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。
https://leetcode.cn/problems/remove-nth-node-from-end-of-list/
"""
from leetcode.basetype import *


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        fake_head = ListNode(0, head)
        fast, slow = head, fake_head
        s = 0
        while s < n:
            fast = fast.next
            s += 1
        while fast is not None:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next  # slow新增加了头节点，所以找到的是倒数n+1个，即删除后一个
        return fake_head.next


if __name__ == '__main__':
    obj = Solution()
    print(obj.removeNthFromEnd(new_list_node([1, 2]), 1))
