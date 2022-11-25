from random import randint

from base_sort import Base


class RandomQuickSort(Base):
    def partition(self, start, end):
        pivot = randint(start, end)
        temp = self.array[end]
        self.array[end] = self.array[pivot]
        self.array[pivot] = temp
        pIndex = start

        for i in range(start, end):
            if self.array[i] <= self.array[end]:
                temp = self.array[i]
                self.array[i] = self.array[pIndex]
                self.array[pIndex] = temp
                pIndex += 1
        temp1 = self.array[end]
        self.array[end] = self.array[pIndex]
        self.array[pIndex] = temp1

        return pIndex

    def sort(self, start=-1, end=-1):
        if start == -1:
            start = 0
        if end == -1:
            end = len(self.array) - 1

        if start < end:
            pIndex = self.partition(start, end)
            self.sort(start, pIndex - 1)
            self.sort(pIndex + 1, end)
