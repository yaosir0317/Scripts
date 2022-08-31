from typing import Optional

from leetcode.basetype import ListNode, new_list_node


"""
给你两个非空 的链表，表示两个非负的整数。它们每位数字都是按照逆序的方式存储的，并且每个节点只能存储一位数字。
请你将两个数相加，并以相同形式返回一个表示和的链表。
"""


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        ret = None
        cursor = None
        carry = 0
        while l1 is not None or l2 is not None:
            if l1 is not None:
                num1 = l1.val
                l1 = l1.next
            else:
                num1 = 0
            if l2 is not None:
                num2 = l2.val
                l2 = l2.next
            else:
                num2 = 0
            v = (num1 + num2 + carry) % 10
            c = (num1 + num2 + carry) // 10
            carry = c
            if cursor is None:
                ret = ListNode(v)
                cursor = ret
            else:
                cursor.next = ListNode(v)
                cursor = cursor.next
        if carry != 0:
            cursor.next = ListNode(carry)
        return ret


if __name__ == '__main__':
    obj = Solution()
    l1 = new_list_node([2, 4, 3])
    l2 = new_list_node([5, 6, 4])
    obj.addTwoNumbers(l1, l2)

    l11 = new_list_node([1])
    l22 = new_list_node([9])
    obj.addTwoNumbers(l11, l22)

    l111 = new_list_node([9,9,9,9,9,9,9])
    l222 = new_list_node([9,9,9,9])
    obj.addTwoNumbers(l111, l222)