class Solution(object):
    def merge_sort(self, l: list):
        if len(l) < 2:
            return l
        mid = len(l) // 2
        return self.merge(self.merge_sort(l[0: mid]), self.merge_sort(l[mid:]))

    def merge(self, left: list, right: list) -> list:
        ret = list()
        left_index = 0
        right_index = 0
        while left_index < len(left) and right_index < len(right):
            if left[left_index] <= right[right_index]:
                ret.append(left[left_index])
                left_index += 1
            else:
                ret.append(right[right_index])
                right_index += 1
        if left_index < len(left):
            ret.extend(left[left_index:])
        if right_index < len(right):
            ret.extend(right[right_index:])
        return ret

    def merge_sort_two(self, l1: list, l2: list):
        return self.merge(self.merge_sort(l1), self.merge_sort(l2))


if __name__ == '__main__':
    pass
