from base_sort import Base


class SelectionSort(Base):
    def __init__(self):
        super().__init__()

    def sort(self):
        size = len(self.array)
        for ind in range(size):
            min_index = ind

            for j in range(ind + 1, size):
                if self.array[j] < self.array[min_index]:
                    min_index = j
            (self.array[ind], self.array[min_index]) = (self.array[min_index], self.array[ind])
