import collections
from pathlib import Path

import numpy as np


def read_simulation_output():
    file_path = Path(__file__).parent / './statistics.csv'
    matrix_output = []
    with open(file_path) as f:
        lis = [line.split() for line in f]
        for i, x in enumerate(lis):
            x.sort()
            matrix_output.append(x)

    return matrix_output


def find_duplicated_hands():
    a = np.array(read_simulation_output())
    values, counts = np.unique(a, axis=0, return_counts=True)
    return [list(str(counts[i])) + list(values[i]) for i in range(len(counts)) if counts[i] > 1]


best_winner_hands = sorted(find_duplicated_hands(), key=lambda x: x[0])
for best in reversed(best_winner_hands):
    print(best)
