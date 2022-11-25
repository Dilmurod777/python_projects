import random
import time
import sys

from insertion_sort import InsertionSort
from merge_sort import MergeSort
from quick_sort import QuickSort
from radix_sort import RadixSort
from random_quick_sort import RandomQuickSort
from selection_sort import SelectionSort
from bubble_sort import BubbleSort
from heap_sort import HeapSort
from shell_sort import ShellSort
from counting_sort import CountingSort

if __name__ == '__main__':
    N = 1000
    trials = 10
    min_value = 1
    max_value = 1000

    random_x = [random.randint(min_value, max_value + 1) for _ in range(N)]
    sorted_x = sorted(random_x)
    reverse_sorted_x = sorted_x[::-1]
    nearly_random_x = sorted(random_x[0:int(N * 0.7)]) + random_x[int(N * 0.7):]

    sys.setrecursionlimit(2 * N)

    data = {
        "random": random_x,
        "nearly": nearly_random_x,
        "sorted": sorted_x,
        "reverse": reverse_sorted_x
    }

    sorting_algorithms = {
        'InsertionSort': InsertionSort(),
        'SelectionSort': SelectionSort(),
        'BubbleSort': BubbleSort(),
        'HeapSort': HeapSort(),
        'ShellSort': ShellSort(),
        'CountingSort': CountingSort(),
        'QuickSort': QuickSort(),
        'MergeSort': MergeSort(),
        'RadixSort': RadixSort(),
        'RandomQuickSort': RandomQuickSort()
    }

    time_complexities = {}
    for algo in sorting_algorithms:
        time_complexities[algo] = {}
        for data_type in data:
            time_complexities[algo][data_type] = []

    for t in range(trials):
        print(f'Trial {t + 1}...')
        for data_type in data:
            x = data[data_type]
            for algo in sorting_algorithms:
                start = time.time()
                y = sorting_algorithms[algo].run(x)
                end = time.time()
                time_complexities[algo][data_type].append(round((end - start) * 1000, 4))

    title_row = "{:<20}".format('Algorithm')
    for data_type in data:
        title_row += "{:<15}".format(data_type)
    print(title_row)
    print('-' * 75)

    for algo in sorting_algorithms:
        row = "{:<20}".format(algo)
        for data_type in data:
            values = time_complexities[algo][data_type]
            avg = sum(values) / len(values)
            row += "{:<15}".format(round(avg, 4))
        print(row)
