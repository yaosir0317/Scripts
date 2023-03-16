"""
给你一个单链表的头节点 head ，请你判断该链表是否为回文链表。如果是，返回 true ；否则，返回 false 。
https://leetcode.cn/problems/palindrome-linked-list/
"""
from leetcode.basetype import *


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not (head and head.next):
            return True
        fast = head
        slow = head
        rev_slow = None
        while fast and fast.next:
            fast = fast.next.next
            slow_next = slow.next
            slow.next = rev_slow
            rev_slow = slow
            slow = slow_next
        _slow = slow
        if fast and fast.next is None:
            slow = slow.next
        need_rev = rev_slow
        while slow and rev_slow:
            if slow.val == rev_slow.val:
                slow = slow.next
                rev_slow = rev_slow.next
            else:
                return False
        head = None
        while need_rev:
            _next = need_rev.next
            need_rev.next = head
            head = need_rev
            need_rev = _next
        cursor = head
        while cursor.next:
            cursor = cursor.next
        cursor.next = _slow
        return True


if __name__ == '__main__':
    obj = Solution()
    l = new_list_node([1, 2, 4, 4, 2, 1])
    obj.isPalindrome(l)
    print(l)