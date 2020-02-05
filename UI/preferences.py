from PyQt5.QtWidgets import QDialog,QDialogButtonBox,QSlider
from PyQt5.QtCore import Qt,QSettings,QSize,QRect

class settingGUI(QDialog):
    def __init__(self, parent=None):
        super(settingGUI, self).__init__(parent)
        self.configureUI(self)

    def configureUI(self, Dialog):
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle("Settings") 
        
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(150, 250, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.sl_value = QSlider(Dialog)
        self.sl_value.setGeometry(QRect(220, 120, 161, 31))
        self.sl_value.setOrientation(Qt.Horizontal)
        self.sl_value.setObjectName("sl_value")
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.settings = QSettings("Sudoku", 'Sudoku')