"""
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
https://leetcode.cn/problems/merge-two-sorted-lists/
"""
from typing import Optional

from leetcode.basetype import ListNode, new_list_node


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val >= list2.val:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
        else:
            list1.next = self.mergeTwoLists(list2, list1.next)
            return list1


if __name__ == '__main__':
    obj = Solution()
    l1 = new_list_node([1,2,4])
    l2 = new_list_node([1,3,4])
    print(obj.mergeTwoLists(l1, l2))