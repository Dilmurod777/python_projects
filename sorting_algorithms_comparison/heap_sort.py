from base_sort import Base


class HeapSort(Base):
    def heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self.array[i] < self.array[left]:
            largest = left

        if right < n and self.array[largest] < self.array[right]:
            largest = right

        if largest != i:
            (self.array[i], self.array[largest]) = (self.array[largest], self.array[i])
            self.heapify(n, largest)

    def sort(self):
        n = len(self.array)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)

        for i in range(n - 1, 0, -1):
            (self.array[i], self.array[0]) = (self.array[0], self.array[i])
            self.heapify(i, 0)
