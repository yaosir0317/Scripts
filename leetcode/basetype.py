from typing import Optional, List


class ListNode:
    def __init__(self, x, next=None):
        self.val = x
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
