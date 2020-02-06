import sys
from datetime import datetime
from PyQt5.QtCore import (QRect, QSettings, QSize, Qt, QThread, pyqtSignal,
                          pyqtSlot)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QDialog,
                             QDialogButtonBox, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QMainWindow, QMessageBox,
                             QPushButton, QSizePolicy, QSlider, QSpacerItem,
                             QVBoxLayout, QWidget)

from board import Board
#from settings.config import user_settings
from UI.preferences import SettingGUI
from UI.statistics import StatisticsGUI
from UI.tiles import SudokuTile
from UI.importData import Json_handler
from UI.status_bar import Status_bar

class MainWindow_UI(QMainWindow):#QDialog
    def __init__(self, board_base=3, parent = None):
        super(MainWindow_UI, self).__init__(parent)
        self.configs = {
            "users":Json_handler("settings/config.json"),
            "themes":Json_handler("settings/theme.json")
        }
        self.user_settings = self.configs['users'].data['user_settings']
        self.themes = self.configs['themes'].data
        self.global_settings = self.configs['users'].data['global_settings'] 

        self.tiles=[]
        self.solvedTiles=[]
        self.board = None
        self.configureUI()

    def configureUI(self):
        self.setGeometry(300, 300, 250, 220)
        self.setFixedSize(800,800)
        self.setWindowTitle('Sudoko')
        
        # Flags
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Init the status bar
        Status_bar().status_bar(dialog=self)

        # Display GUI
        self.show()

    def modifyTiles(self, tiles=[], solvedTiles=[], solution=False) -> list:
        """
        Create a new set of tiles from the board
        """
        if not self.board == None:
            if not solution:
                tiles = [SudokuTile(tile,self) for row in self.board.tiles for tile in row]
            else: 
                for tile,_ in enumerate(tiles):
                        tiles[tile].updateElement(solvedTiles[tile])

            return tiles

    def update_grid_base(self) -> None:
        """
        If the base is modified this needs to be updated.
        Handled from preferences.py
        """
        print("Updating the base")
        base = self.user_settings['board_base']
        # Layouts
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)

        for i in range(base):
            for j in range(base):
                layout = QGridLayout()
                layout.setSpacing(1)
                self.grid_layout.addLayout(layout, i, j)

        self.central_widget = QWidget()    
        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)     
        

    def updateGrid(self, tiles)->None:
        """
        Update the grid on create and reset board.
        """   
        if self.board == None: return None

        base = self.user_settings['board_base']
        side = base**2

        for i in range(side):
            for j in range(side):
                inner_layout = self.grid_layout.itemAtPosition(i // base, j // base)
                cell = tiles[i * side + j]

                inner_layout.addWidget(cell, i % base, j % base)
                cell.setFocusPolicy(Qt.StrongFocus)
                    
        self.game_time = datetime.now()

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
        self.global_settings['tileSize'] = 0.90*self.geometry().height()//(self.user_settings['board_base']**2) 
        self.board = Board(base=self.user_settings['board_base'], difficulty=self.user_settings['difficulty']) # TODO GUI should scale to board_base
        self.solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
        self.tiles = self.modifyTiles()
        self.update_grid_base()
        self.updateGrid(tiles=self.tiles)
        self.user_settings['statistics']['games'] += 1

    def restartGame(self):
        """
        Reset changed tiles and go back to original board
        """
        print("Restart game")
        self.win = False
        self.tiles = self.modifyTiles(solution=False)
        self.updateGrid(self.tiles)

    def showSolution(self):
        """
        Fill all tiles with solution
        """
        print("Show solution")
        self.tiles = self.modifyTiles(self.tiles,solvedTiles=self.solvedTiles,solution=True)
        
    def checkSolution(self):
        """
        Check if given tiles is correct. Title change to "win"
        """
        if not self.board == None:
            print("Check solution")
            tiles = [tile.element for tile in self.tiles]
            solvedTiles = [tile for row in self.board.solvedTiles for tile in row]
            if tiles == solvedTiles:
                self.user_settings['statistics']['win'] += 1

                time = int((datetime.now()-self.game_time).total_seconds())
                best_time = self.user_settings['statistics']['best_time']
                if best_time > time or best_time == 0:
                    print("Game time:", time)
                    self.user_settings['statistics']['best_time'] = time
                    
                self.display_popup("Solution sheet","Congratulations! You managed to finish the game! Your game time is: " + str(time) + " seconds")

            else:
                self.display_popup("Solution sheet","Unfortunately, but the solution is not correct! Try again and check if you got correct answer!")


    def openSettings(self):
        """
        Open settings menu
        """
        print("Update settings")
        self.settingGUI = SettingGUI(self)
        self.settingGUI.show()
        self.settingGUI.exec_

    def openStatistics(self):
        print("Update statistics")
        self.statisticsGUI = StatisticsGUI(self)
        self.statisticsGUI.show()
        self.statisticsGUI.exec_

    def display_popup(self, title, message)->None:
        msg = QMessageBox()
        msg.setWindowTitle(str(title))
        msg.setText(str(message)) 
        msg.exec_()

        

    def keyPressEvent(self, event):
        """
        Event handler
        """
        events = {
            Qt.Key_Escape:self.quit,
            Qt.Key_F1:self.restartGame,
            Qt.Key_F2:self.newGame,
            Qt.Key_F3:self.showSolution,
            Qt.Key_F4:self.checkSolution,
            Qt.Key_F5:self.openSettings,
        }
        if event.key() in events:
            events[event.key()]()

        
    def update(self): 
        theme = self.user_settings['theme']
        self.setStyleSheet(" ".join(self.themes[theme]['widget_background'])) #<-- Broken changes UI TODO: FIX IT
        
    def quit(self):
        self.configs['users'].saveConfig()
        sys.exit()  
