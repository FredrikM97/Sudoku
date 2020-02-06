from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SudokuTile(QLabel):
    """
    Single sudoku tile
    """
    def __init__(self, element=0, parent=None):
        super(SudokuTile,self).__init__(parent)
        self.parent = parent
        # Set property of tile
        self.element = element
        self.isStatic = self.element > 0 
        self.init()

    def init(self):
        """
        Init of tile
        """
        
        self.colorTile()
        self.setText(str(self.element))
        self.setAlignment(Qt.AlignCenter)

        tileSize = self.parent.global_settings['tileSize']
        self.setFixedSize(tileSize, tileSize)
        textSize = 25*tileSize//self.parent.global_settings['default_tileSize'] #"font-size:25pt;",
        self.setFont(QFont('Ubuntu', textSize))

    def colorTile(self):
        """
        Modify the color of a tile
        """
        theme_type = self.parent.user_settings['theme']
        theme = self.parent.themes[theme_type]
        
        if self.isStatic:
            sheet_type = 'static_tile'

        elif self.element == 0: # If empty
            # Focus on empty tile
            if self.hasFocus():
                sheet_type = 'focused_empty_tile'
            else:
                sheet_type = 'empty_tile'
        else:
            # Focus on edited tile
            if self.hasFocus():
                sheet_type = 'focus_dynamic'
            else:
                sheet_type = 'dynamic'
                
        self.setStyleSheet(" ".join(theme[sheet_type]))

        info = "not " if self.isStatic else ""
        self.setStatusTip("This tile is "+ info + "Editable")

    def updateElement(self, element=0):
        """
        Update element at focused tile
        """
        if not self.isStatic:
            self.element = element
            self.setText(str(self.element))
            self.colorTile()


    def focusInEvent(self, event):
        self.colorTile()    

    def focusOutEvent(self, event):
        self.colorTile()

    def keyPressEvent(self, event):
        """
        Handles keypresses
        """
        if event.key() <= Qt.Key_9 and event.key() >= Qt.Key_0:
            self.updateElement(event.key() - Qt.Key_0)
        else:
            self.parent.keyPressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Check if tile is removed 
        """
        if (event.button() == Qt.RightButton):
            self.updateElement(0)