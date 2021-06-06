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
            return ' '
    
        if self.state == State.FLAGGED:
            return '⚑'
    
        if self.hasMine:
            return '💣'
    
        if self.minesAround != 0:
            return str(self.minesAround)
    
        return ' '



class Field:
    DELTAS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def __init__(self, rows, columns):
        # տողերի քանակը
        self.rows = rows
        # սյուների քանակը
        self.columns = columns

        # ականակետերի մատրիցը
        self.cells = [[Cell() for c in range(self.columns)] for r in range(self.rows)]
        # տեղադրել ականները և կատարել հաշվարկները
        self._placeAllMines()

        # քայլերի հաշվիչ
        self.stepsCounter = 0


    # ականների տաղադրելը պատահական վանդակներում
    def _placeAllMines(self):
        self.minesCount = int(self.rows * self.columns * 15 / 100)
        for m in range(self.minesCount):
            r, c = self._placeRandomMine()
            self._updateNumbersAround(r, c)


    # տեղադրել պատահական ական ու վերադարձնել դրա դիրքը
    def _placeRandomMine(self):
        r = random.randint(0, self.rows - 1)
        c = random.randint(0, self.columns - 1)

        if not self.cells[r][c].hasMine:
            self.cells[r][c].hasMine = True
            return (r, c)

        return self._placeRandomMine()


    # թարմացնել ականին շրջապատող վանդակների թվերը
    def _updateNumbersAround(self, row, column):
        for (dr, dc) in Field.DELTAS:
            nr, nc = row + dr, column + dc
            if nr in range(self.rows) and nc in range(self.columns):
                self.cells[nr][nc].minesAround += 1


    # բացել վանդակը
    def open(self, row, column, count = True):
        # վերցնել վանդակի հղումը
        cell = self.cells[row][column]
        # եթե վանդակը փակ է, ...
        if cell.state == State.CLOSED:
            # ... ապա բացել այն
            cell.state = State.OPEN

            # եթե պարզվում է, որ վանդակում ական կա, ...
            if cell.hasMine:
                # ... ապա բացել բոլոր ականներն ու ...
                for r in range(self.rows):
                    for c in range(self.columns):
                        if self.cells[r][c].hasMine:
                            self.cells[r][c].state = State.OPEN
                # ... ավարտել խաղը
                self.gameOver = True
            else:
                # եթե վանդակում ական չկա, ...
                # ... և նրա հարևաններում էլ ականներ չկան, ...
                # ... ապա բացել նաև հարևաններին
                if cell.minesAround == 0:
                    for (dr, dc) in Field.DELTAS:
                        r = row + dr
                        c = column + dc
                        if r in range(self.rows) and c in range(self.columns):
                            self.open(r, c, False)
            # մեկ քայլ
            if count:
                self.stepsCounter += 1


    # դրոշակով նշել վանդակը
    def flag(self, row, column):
        # վերցնել վանդակի հղումը
        cell = self.cells[row][column]
        # եթե վանդակը փակ է, ապա այն նշել դրոշակով
        if cell.state == State.CLOSED:
            cell.state = State.FLAGGED
        # եթե արդեն նշված է դրոշակով, ապա հանդել այն
        elif cell.state == State.FLAGGED:
            cell.state = State.CLOSED

