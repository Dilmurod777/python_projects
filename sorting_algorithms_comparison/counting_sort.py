from base_sort import Base


class CountingSort(Base):
    def sort(self, *args):
        size = len(self.array)
        max_value = max(self.array) + 1
        output = [0] * size

        count = [0] * max_value

        for m in range(0, size):
            count[self.array[m]] += 1

        for m in range(1, max_value):
            count[m] += count[m - 1]

        m = size - 1
        while m >= 0:
            output[count[self.array[m]] - 1] = self.array[m]
            count[self.array[m]] -= 1
            m -= 1

        for m in range(0, size):
            self.array[m] = output[m]
