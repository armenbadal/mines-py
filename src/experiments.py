
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLCDNumber, QLabel, QMainWindow, QPushButton, QSpacerItem, QVBoxLayout, QWidget


class W(QMainWindow):
    def __init__(self):
        super(W, self).__init__()

        self.sec = 0

        self._createUi()
        self._setupTimer()

    def _createUi(self):
        base = QWidget(self)
        vbox = QVBoxLayout(base)
        vbox.setContentsMargins(2, 2, 2, 2)

        upper = QWidget(base)
        hbox = QHBoxLayout(upper)
        hbox.setContentsMargins(2, 2, 2, 2)
        self.steps = QLabel('0')
        hbox.addWidget(self.steps)
        hbox.addStretch(1)
        self.seconds = QLCDNumber()
        self.seconds.setDigitCount(3)
        hbox.addWidget(self.seconds)
        upper.setLayout(hbox)
        vbox.addWidget(upper)

        lower = QWidget(base)
        grid = QGridLayout(lower)
        grid.setSpacing(1)
        grid.setContentsMargins(2, 2, 2, 2)
        grid.addWidget(QPushButton('1'), 0, 0)
        grid.addWidget(QPushButton('2'), 0, 1)
        grid.addWidget(QPushButton('3'), 0, 2)
        grid.addWidget(QPushButton('4'), 0, 3)
        grid.addWidget(QPushButton('1'), 1, 0)
        grid.addWidget(QPushButton('2'), 1, 1)
        grid.addWidget(QPushButton('3'), 1, 2)
        grid.addWidget(QPushButton('4'), 1, 3)
        lower.setLayout(grid)
        vbox.addWidget(lower)

        base.setLayout(vbox)

        self.setCentralWidget(base)


    def _setupTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._updateSeconds)
        self.timer.start(1000)


    def _updateSeconds(self):
        self.sec += 1
        self.seconds.display(str(self.sec))


app = QApplication(sys.argv)
w = W()
w.show()
sys.exit(app.exec_())
