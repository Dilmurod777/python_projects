from base_sort import Base


class MergeSort(Base):
    def merge(self, left, middle, right):
        n1 = middle - left + 1
        n2 = right - middle

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = self.array[left + i]

        for j in range(0, n2):
            R[j] = self.array[middle + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            self.array[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            self.array[k] = R[j]
            j += 1
            k += 1

    def sort(self, left=-1, right=-1):
        if left == -1:
            left = 0
        if right == -1:
            right = len(self.array) - 1

        if left < right:
            m = left + (right - left) // 2

            self.sort(left, m)
            self.sort(m + 1, right)
            self.merge(left, m, right)
