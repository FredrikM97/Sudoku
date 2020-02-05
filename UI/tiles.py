from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class SudokuTile(QLabel):
    """
    Single sudoku tile
    """
    def __init__(self, element=0 , parent=None):
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
        self.setFixedSize(60, 60)
    
    def colorTile(self):
        """
        Modify the color of a tile
        """
        theme = self.parent.settings['theme']
        if self.isStatic:
            self.setStyleSheet(theme.static_tile)

        elif self.element == 0: # If empty
            # Focus on empty tile
            if self.hasFocus():
                self.setStyleSheet(theme.focused_empty_tile)
            else:
                self.setStyleSheet(theme.empty_tile)
        else:
            # Focus on edited tile
            if self.hasFocus():
                self.setStyleSheet(theme.focus_dynamic)
            else:
                self.setStyleSheet(theme.dynamic)
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
        #print("Got focus")

    def focusOutEvent(self, event):
        self.colorTile()
        #print("Lost focus")

    def keyPressEvent(self, event):
        """
        Handles keypresses
        """
        if event.key() <= Qt.Key_9 and event.key() >= Qt.Key_0:
            self.updateElement(event.key() - Qt.Key_0)
        else:
            self.parent.keyPressEvent(event)
        print("keypress",event.key())

    def mouseReleaseEvent(self, event):
        """
        Check if tile is removed 
        """
        if (event.button() == Qt.RightButton):
            self.updateElement(0)