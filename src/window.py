
from mines import Field, State
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QMainWindow, QMenu, QMenuBar, QWidget

#
# Մեկ ականի վանդակը որպես QLabel-ի ընդլայնում
#
class Place(QLabel):
    open = Signal(int, int)
    flag = Signal(int, int)

    def __init__(self, row, column):
        super().__init__()

        self.row = row
        self.column = column

        self.setMinimumSize(32, 32)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised) # Sunken
        self.setLineWidth(2)
        self.setAlignment(Qt.AlignCenter)

        self.setText(' ')


    # որոշել բջջի պարունակությունն ու վիճակը
    def setData(self, state, data):
        if state == State.OPEN:
            self.setFrameShadow(QFrame.Sunken)
        self.setText(data)


    # մկնիկի գործողությունների արտապատկերումը սեփական Signal-ների
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open.emit(self.row, self.column)
        elif event.button() == Qt.RightButton:
            self.flag.emit(self.row, self.column)


#
# Հիմնական պատուհանը որպես QMainWindow-ի ընդլայնում
#
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = Field(10, 16)

        self.setWindowIcon(QIcon('main-icon.png'))
        self.setWindowTitle('Ականներ')

        self._createActions()
        self._createMainMenu()
        self.setCentralWidget(self._createBoard(self.model.rows, self.model.columns))


    @Slot()
    def newGame(self):
        self.model = Field(10, 16)
        for row in self.places:
            for place in row:
                place.setFrameShadow(QFrame.Raised)
        self._updateView()


    def _createBoard(self, rows, columns):
        board = QWidget(self)

        grid = QGridLayout(board)
        grid.setSpacing(0)
        grid.setContentsMargins(2, 2, 2, 2)
        
        self.places = []
        for r in range(rows):
            rw = []
            for c in range(columns):
                pl = Place(r, c)
                pl.open.connect(self.opened)
                pl.flag.connect(self.flagged)
                rw.append(pl)
                grid.addWidget(pl, r, c)
            self.places.append(rw)
            
        return board


    def _createActions(self):
        self.actNew = QAction('Նոր', self)
        self.actNew.triggered.connect(self.newGame)

        self.actEnd = QAction('Ելք', self)
        self.actEnd.triggered.connect(self.close)

        self.actAbout = QAction('Խաղի մասին', self)
        #connect(actAbout, SIGNAL(triggered()), this, SLOT(aboutGame()));


    def _createMainMenu(self):
        mainMenu = QMenuBar(self)

        mnuGame = QMenu('Խաղ', mainMenu)
        mainMenu.addAction(mnuGame.menuAction())
        mnuGame.addAction(self.actNew)
        mnuGame.addSeparator()
        mnuGame.addAction(self.actEnd)

        mnuHelp = QMenu('Հուշում', mainMenu)
        mainMenu.addAction(mnuHelp.menuAction())
        mnuHelp.addAction(self.actAbout)

        self.setMenuBar(mainMenu)


    def _updateView(self):
        for r in range(self.model.rows):
            for c in range(self.model.columns):
                cell = self.model.cells[r][c]
                self.places[r][c].setData(cell.state, str(cell))


    @Slot(int, int)
    def opened(self, row, column):
        self.model.open(row, column)
        self._updateView()

    @Slot(int, int)
    def flagged(self, row, column):
        self.model.flag(row, column)
        self._updateView()
