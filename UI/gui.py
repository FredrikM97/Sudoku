from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt,pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import *

from board import Board
from Theme.default import defaultTheme
from .tiles import SudokuTile

class mainGUI(QDialog):
    eventModified = pyqtSignal(object, name='eventModified') 
    def __init__(self, theme = defaultTheme(), parent = None):
        super().__init__()
        self.theme = theme
        self.board = None
        self.configureUI()
        self.win = False
        self.newGame()


    def configureUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Sudoko')

        # Layouts
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)

        for i in range(3): # TODO check if 3x3 grid is correct for part of Sudoku
            for j in range(3):
                layout = QGridLayout()
                layout.setSpacing(1)
                self.grid_layout.addLayout(layout, i, j)

        # Add to screen
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)



    def createTiles(self, solution=False):
        """
        Create a new set of tiles from the board
        """
        if not solution:
            self.tiles = [SudokuTile(tile, self.theme,self) for row in self.board.tiles for tile in row]
        else: 
            # TODO: Need a hotfix for performance, should keep possibility for edits even after solution given
            solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
            for tile,_ in enumerate(self.tiles):
                    self.tiles[tile].updateElement(solvedTiles[tile])
            
    def updateGrid(self):
        # TODO: Rework this ugly solution
        side = self.board.side
        base = self.board.base
        for i in range(side):
            for j in range(side):

                inner_layout = self.grid_layout.itemAtPosition(i // base, j // base)
                cell = self.tiles[i * side + j]
                inner_layout.addWidget(cell, i % base, j % base)
                cell.setFocusPolicy(Qt.StrongFocus)
                self.update()

    def menu(self):
        """
        Display a menu 
        """
        pass
    
    def display_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def newGame(self):
        """
        Create a new board
        """
        print("New Game")
        self.board = Board()
        self.win = False
        self.createTiles()
        self.updateGrid()
        

    def showSolution(self):
        """
        Fill all tiles with solution
        """
        print("Show solution")
        self.createTiles(solution=True)
        self.updateGrid()
    
    def checkSolution(self):
        """
        Check if given tiles is correct. Title change to "win"
        """
        print("Check solution")
        tiles = [tile.element for tile in self.tiles]
        solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
        if tiles == solvedTiles:
            self.display_popup("Solution sheet","Congratulations! You managed to finish the game!")
            print("You won!")
        else:
            self.display_popup("Solution sheet","Unfortunately, but the solution is not correct! Try again and check if you got correct answer!")
            print("That is not correct solution!")
        print(tiles, solvedTiles)
        
    def restartGame(self):
        """
        Reset changed tiles and go back to original board
        """
        print("Restart game")
        self.win = False
        self.createTiles(solution=False)
        self.updateGrid()
    
    def keyPressEvent(self, event):
        events = {
            Qt.Key_Escape:self.quit,
            Qt.Key_F1:self.restartGame,
            Qt.Key_F2:self.newGame,
            Qt.Key_F3:self.showSolution,
            Qt.Key_F4:self.checkSolution,
        }
        if event.key() in events:
            events[event.key()]()
        print("Current event",event.key())
        
    @pyqtSlot()
    def update(self): 
        self.setStyleSheet(self.theme.widget_background)


    @pyqtSlot()
    def quit(self):
        self.exit()  
             
