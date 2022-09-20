from leetcode.basetype import *


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cursor = head
        new = None
        while cursor:
            next = cursor.next
            cursor.next = new
            new = cursor
            cursor = next
        return new