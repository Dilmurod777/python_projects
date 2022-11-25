from base_sort import Base


class ShellSort(Base):
    def sort(self):
        n = len(self.array)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.array[i]

                j = i
                while j >= gap and self.array[j - gap] > temp:
                    self.array[j] = self.array[j - gap]
                    j -= gap

                self.array[j] = temp
            gap //= 2
