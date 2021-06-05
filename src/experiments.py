
import random

class Cell:
    def __init__(self):
        self.number = random.randint(0, 100)

    def __str__(self):
        return str(self.number)


ROWS = 10
COLUMNS = 16
DELTAS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

mx = [[Cell() for c in range(COLUMNS)] for r in range(ROWS)]

def countGreaterThan(row, column, val):
    return list(filter(lambda rc: mx[rc[0]][rc[1]].number > val,
                    filter(lambda rc: rc[0] in range(ROWS) and rc[1] in range(COLUMNS),
                           map(lambda rc: (row + rc[0], column + rc[1]), DELTAS))))


k = countGreaterThan(0, 0, 50)
print(k)
