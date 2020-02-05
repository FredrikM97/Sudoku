from PyQt5.QtWidgets import QApplication,QSpacerItem,QDialogButtonBox,QPushButton, QAction,QSlider,QSizePolicy,QMessageBox,QCheckBox,QMainWindow,QLabel, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt,pyqtSignal, QThread, pyqtSlot,QSettings,QSize,QRect
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from board import Board
from UI.tiles import SudokuTile
from settings.config import user_settings
from UI.preferences import settingGUI

class MainWindow_UI(QMainWindow):#QDialog
    def __init__(self, board_base=3, parent = None):
        super(MainWindow_UI, self).__init__(parent)
        self.settings = user_settings
        
        self.board = None
        self.configureUI()
        #self.newGame()


    def configureUI(self):
        self.setGeometry(300, 300, 250, 220)
        self.setWindowTitle('Sudoko')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Layouts
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)

        # Add to screen
        self.updateBase()
        self.central_widget = QWidget()    
        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)
        
        # Init the status bar
        self.status_bar()

        # Display GUI
        self.show()

    def status_action(self, name, shortCut, statusTip, trigger):
        action = QAction(name, self) 
        action.setShortcut(shortCut)
        action.setStatusTip(statusTip)
        if not trigger == None:
            action.triggered.connect(trigger)
        return action

    def status_bar(self):
        """
        Add statusbar to the menu
        """
        newGame = self.status_action("New game", "Ctrl+N", "Start new game", self.newGame)
        resetGame = self.status_action("Reset game", "Ctrl+R", "Reset game", self.restartGame)
        getSolution = self.status_action("Solution", "Ctrl+S", "Get the solution", self.showSolution)
        exitGame = self.status_action("Exit", "Ctrl+Q", "Exit the App", self.quit)
        settingsGame = self.status_action("Settings", "Ctrl+E", "Show settings", self.showSettings)
        infoGame = self.status_action("Info", "Ctrl+I", "Show info", lambda titl="Information", message="Made by FredrikM97": self.display_popup(titl, message))
        self.statusBar()
        mainMenu = self.menuBar()

        menu = [mainMenu.addMenu(index) for index in ['&File', '&Edit','&Info']]
        action = [[newGame, resetGame, getSolution, exitGame],[settingsGame],[infoGame]]

        # Add actions to GUI
        for index,name in enumerate(menu):
            for info in action[index]:
                name.addAction(info)

    def createTiles(self, solution=False):
        """
        Create a new set of tiles from the board
        """
        if not self.board == None:
            if not solution:
                self.tiles = [SudokuTile(tile,self) for row in self.board.tiles for tile in row]
                print("length of tiles:",len(self.tiles))
            else: 
                # TODO: Need a hotfix for performance, should keep possibility for edits even after solution given
                for tile,_ in enumerate(self.tiles):
                        self.tiles[tile].updateElement(self.solvedTiles[tile])
    def updateBase(self):
        print("Updating the base")
        base = self.settings['board_base']
        for i in range(base):
            for j in range(base):
                layout = QGridLayout()
                layout.setSpacing(1)
                self.grid_layout.addLayout(layout, i, j)


    def updateGrid(self):
        # TODO: Rework this ugly solution
        if not self.board == None:            
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
        msg.setWindowTitle(str(title))
        msg.setText(str(message)) 
        msg.exec_()

    def newGame(self):
        """
        Create a new board
        """
        print("New Game")
        self.board = Board(base=self.settings['board_base'], difficulty=self.settings['difficulty']) # TODO GUI should scale to board_base
        self.solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
        self.win = False
        self.createTiles()
        self.updateGrid()
        self.board.pretty_prints()
        

    def showSolution(self):
        """
        Fill all tiles with solution
        """
        print("Show solution")
        self.createTiles(solution=True)
        #self.updateGrid()
    
    def checkSolution(self):
        """
        Check if given tiles is correct. Title change to "win"
        """
        print("Check solution")
        tiles = [tile.element for tile in self.tiles]
        solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
        if tiles == solvedTiles:
            self.display_popup("Solution sheet","Congratulations! You managed to finish the game!")

        else:
            self.display_popup("Solution sheet","Unfortunately, but the solution is not correct! Try again and check if you got correct answer!")
  
        print(tiles, solvedTiles)
        
    def restartGame(self):
        """
        Reset changed tiles and go back to original board
        """
        print("Restart game")
        self.win = False
        self.createTiles(solution=False)
        self.updateGrid()

    def showSettings(self):
        print("Update settings")
        self.settingGUI = settingGUI(self)
        self.settingGUI.show()
        self.settingGUI.exec_

    def keyPressEvent(self, event):
        events = {
            Qt.Key_Escape:self.quit,
            Qt.Key_F1:self.restartGame,
            Qt.Key_F2:self.newGame,
            Qt.Key_F3:self.showSolution,
            Qt.Key_F4:self.checkSolution,
            Qt.Key_F5:self.showSettings,
        }
        if event.key() in events:
            events[event.key()]()

        
    @pyqtSlot()
    def update(self): 
        theme = self.settings['theme']
        self.setStyleSheet(theme.widget_background)


    @pyqtSlot()
    def quit(self):
        sys.exit()  
             
