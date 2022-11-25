from base_sort import Base


class InsertionSort(Base):
    def sort(self):
        for i in range(1, len(self.array)):

            key = self.array[i]

            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
