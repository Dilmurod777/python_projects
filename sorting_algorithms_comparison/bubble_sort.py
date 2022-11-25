from base_sort import Base


class BubbleSort(Base):
    def __init__(self):
        super().__init__()

    def sort(self):
        n = len(self.array)
        swapped = False
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    swapped = True
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]

            if not swapped:
                return
