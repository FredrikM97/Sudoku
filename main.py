from PyQt5.QtWidgets import QApplication
from board import Board
from UI.gui import mainGUI
import sys

def main():
    init_GUI()

def init_GUI():
    app = QApplication(sys.argv)
    game = mainGUI()
    game.show()
    sys.exit(app.exec_())

def init_board():
    board = Board(base=3)
    print("Board:")
    board.pretty_prints(board.tiles)
    print("Solved board:")
    board.pretty_prints(board.solvedTiles)


if __name__ == "__main__":
    main()