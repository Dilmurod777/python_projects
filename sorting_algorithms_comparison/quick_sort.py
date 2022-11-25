from base_sort import Base


class QuickSort(Base):
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] <= pivot:
                i = i + 1
                (self.array[i], self.array[j]) = (self.array[j], self.array[i])
        (self.array[i + 1], self.array[high]) = (self.array[high], self.array[i + 1])
        return i + 1

    def sort(self, low=-1, high=-1):
        if low == -1:
            low = 0
        if high == -1:
            high = len(self.array) - 1

        if low < high:
            pi = self.partition(low, high)

            self.sort(low, pi - 1)
            self.sort(pi + 1, high)
