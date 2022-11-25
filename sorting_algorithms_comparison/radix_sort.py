from base_sort import Base


class RadixSort(Base):
    def modified_counting_sort(self, exp):
        n = len(self.array)
        output = [0] * n
        count = [0] * 10

        for i in range(0, n):
            index = self.array[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = self.array[i] // exp
            output[count[index % 10] - 1] = self.array[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(0, n):
            self.array[i] = output[i]

    def sort(self, *args):
        max_value = max(self.array)

        exp = 1
        while max_value // exp > 0:
            self.modified_counting_sort(exp)
            exp *= 10
