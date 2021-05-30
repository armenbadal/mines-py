
import sys
from PySide6.QtWidgets import QApplication
from window import Window
from mines import Field

#
def main():
    app = QApplication(sys.argv)

    game = Field(10, 10)
    win = Window(game)
    win.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
