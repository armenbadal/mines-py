
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QMainWindow, QMenu, QMenuBar, QWidget


class Place(QLabel):
    open = Signal(int, int)
    flag = Signal(int, int)

    def __init__(self, row, column):
        super().__init__()

        self.row = row
        self.column = column

        self.setMinimumSize(32, 32)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)
        self.setAlignment(Qt.AlignCenter)

        self.setText('?')

    def setData(self, data):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open.emit(self.row, self.column)
        elif event.button() == Qt.RightButton:
            self.flag.emit(self.row, self.column)


class Window(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.model = model

        self.setWindowTitle('Ականներ')
        self.createMainMenu()
        self.setCentralWidget(self.createBoard(model.rows, model.columns))


    def createBoard(self, rows, columns):
        board = QWidget(self)

        grid = QGridLayout(board)
        grid.setSpacing(1);
        grid.setContentsMargins(1, 1, 1, 1);
        
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

    
    def createMainMenu(self):
        mainMenu = QMenuBar(self)

        mnuGame = QMenu('Խաղ', mainMenu)
        mainMenu.addAction(mnuGame.menuAction())
        #mnuGame->addAction(actNew);
        #mnuGame->addSeparator();
        #mnuGame->addAction(actEnd);

        mnuHelp = QMenu('Հուշում', mainMenu)
        mainMenu.addAction(mnuHelp.menuAction())
        #mnuHelp->addAction(actAbout);

        self.setMenuBar(mainMenu)


    def updateView(self):
        for r in range(self.model.rows):
            for c in range(self.model.columns):
                txt = self.model.getData(r, c)
                self.places[r][c].setText(txt)
    

    @Slot(int, int)
    def opened(self, row, column):
        self.model.open(row, column)
        self.updateView()

    @Slot(int, int)
    def flagged(self, row, column):
        self.model.flag(row, column)
        self.updateView()
        

