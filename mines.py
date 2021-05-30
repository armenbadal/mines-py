import enum
import random

class State(enum.Enum):
    OPEN = 1
    CLOSED = 2
    FLAGGED = 3

class Cell:
    def __init__(self):
        self.state = State.CLOSED
        self.hasMine = False
        self.minesAround = 0

    def __str__(self):
        if self.state == State.CLOSED:
            return '?'

        if self.state == State.FLAGGED:
            return '⚑'

        if self.hasMine:
            return '💣'

        return ' ' if self.minesAround == 0 else str(self.minesAround)


class Field:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

        self.cells = []
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                row.append(Cell())
            self.cells.append(row)

        self.minesCount = int(self.rows * self.columns * 15 / 100)
        for m in range(self.minesCount):
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            self.cells[r][c].hasMine = True

        nbix = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for r in range(self.rows):
            for c in range(self.columns):
                if self.cells[r][c].hasMine:
                    continue

                count = 0
                for (dr, dc) in nbix:
                    nr = r + dr
                    nc = c + dc
                    if nr in range(self.rows) and nc in range(self.columns):
                        if self.cells[nr][nc].hasMine:
                            count += 1
                self.cells[r][c].minesAround = count


    def forEachCell(self, action):
        for r in range(self.rows):
            for c in range(self.columns):
                action(self.cells[r][c])


    def open(self, row, column):
        cell = self.cells[row][column]
        if cell.state == State.CLOSED:
            cell.state = State.OPEN

            if cell.hasMine:
                def g(c): c.state = State.OPEN
                self.forEachCell(g)

                #for r in range(self.rows):
                #    for c in range(self.columns):
                #        if self.cells[r][c].hasMine:
                #            self.cells[r][c].state = State.OPEN

            if not cell.hasMine and cell.minesAround == 0:
                for (dr, dc) in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                    r = row + dr
                    c = column + dc
                    if r in range(self.rows) and c in range(self.columns):
                        self.open(r, c)



    def flag(self, row, column):
        cell = self.cells[row][column]
        if cell.state == State.CLOSED:
            cell.state = State.FLAGGED
        elif cell.state == State.FLAGGED:
            cell.state = State.CLOSED


    def getData(self, row, column):
        return str(self.cells[row][column])

