from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout,QLabel
from PyQt5.QtCore import Qt,pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import *

from board import Board
from Theme.default import defaultTheme

class SudokuTile(QLabel):
    """
    Single sudoku tile
    """
    def __init__(self, element=0 ,theme = defaultTheme(), parent=None):
        super().__init__()
        self.parent = parent
        # Load theme
        self.theme = theme
        # Set property of tile
        self.element = element
        self.isStatic = self.element > 0 
        self.init()

    def init(self):
        """TODO"""
        self.colorTile()
        self.setText(str(self.element))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(60, 60)
    
    def colorTile(self):
        """TODO"""
        if self.isStatic:
            self.setStyleSheet(self.theme.static_tile)

        elif self.element == 0: # If empty
            if self.hasFocus():
                self.setStyleSheet(self.theme.focused_empty_tile)
            else:
                self.setStyleSheet(self.theme.empty_tile)
        else:
            if self.hasFocus():
                self.setStyleSheet(self.theme.focus_dynamic_ss)
            else:
                self.setStyleSheet(self.theme.dynamic_ss)

    def updateElement(self, element=0):
        """TODO"""
        if not self.isStatic:
            self.element = element
            self.setText(str(self.element))
            self.colorTile()
            #self.update()
            self.parent.eventModified.emit(self) # Notify parent classes

    def focusInEvent(self, event):
        self.colorTile()    
        #print("Got focus")

    def focusOutEvent(self, event):
        self.colorTile()
        #print("Lost focus")

    def keyPressEvent(self, event):
        """TODO"""
        if event.key() <= Qt.Key_9 and event.key() >= Qt.Key_0:
            self.updateElement(event.key() - Qt.Key_0)
        else:
            self.parent.keyPressEvent(event)
        print("keypress",event.key())

    def mouseReleaseEvent(self, event):
        """TODO"""
        if (event.button() == Qt.RightButton):
            self.updateElement(0)


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
        print("Debug1")
        for i in range(3): # TODO check if 3x3 grid is correct for part of Sudoku
            for j in range(3):
                layout = QGridLayout()
                layout.setSpacing(1)
                self.grid_layout.addLayout(layout, i, j)
        print("Debug2")

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
        
    def restartGame(self):
        """
        Reset changed tiles and go back to original board
        """
        print("Restart game")
        self.createTiles(solution=False)
        self.updateGrid()
    
    def keyPressEvent(self, event):
        events = {
            Qt.Key_Escape:self.quit,
            Qt.Key_F1:self.restartGame,
            Qt.Key_F2:self.newGame,
            Qt.Key_F3:self.showSolution,
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
             
