from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

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
        """
        Update element at focused tile
        """
        if not self.isStatic:
            self.element = element
            self.setText(str(self.element))
            self.colorTile()
            self.parent.eventModified.emit(self) # Notify parent classes

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