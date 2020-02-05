from PyQt5.QtWidgets import QDialog,QDialogButtonBox,QSlider, QPushButton, QGridLayout, QGroupBox, QLabel,QComboBox, QCheckBox, QSpinBox, QSlider
from PyQt5.QtCore import Qt,QSettings,QSize,QRect
import sys, inspect


from settings.config import user_settings, default_settings
import settings.theme

class settingGUI(QDialog):
    def __init__(self, parent=None):
        super(settingGUI, self).__init__(parent)
        self.parent = parent
        self.modules = [item for item in self.get_modules()]
        self.user_settings = parent.settings
        self.configureUI(self)

    def configureUI(self, Dialog):
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle("Settings") 

        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        
        layout.addWidget(QLabel("Theme:"),0,0) # QComboBox
        layout.addWidget(QLabel("Dark Theme:"),1,0) # QCheckBox
        layout.addWidget(QLabel("Difficulty:"),2,0) # QSpinBox
        layout.addWidget(QLabel("board_base"),3,0) # Slider
        print(self.get_modules())
        layout.addWidget(self.define_combobox(),0,1)
        layout.addWidget(self.define_checkbox(),1,1)
        layout.addWidget(self.define_spinbox(),2,1)
        layout.addWidget(self.define_slider(),3,1)
        layout.addWidget(QLabel("Create a new game in order for difficulty and board base to update"),4,0)

        self.horizontalGroupBox.setLayout(layout)

        self.setLayout(layout)
    
    def define_combobox(self): # Theme setting
        box = QComboBox()

        box.addItems([y[0] for y in self.modules])
        
        box.setCurrentIndex([y[0] for y in self.modules].index(str(self.user_settings['theme'].__name__)))
        
        set_config = lambda: self.update_config('theme', [y[1] for y in self.modules][box.currentIndex()]) 
        print("Debugging:", self.user_settings['theme'], [y[1] for y in self.modules][box.currentIndex()])
        box.currentIndexChanged.connect(set_config)
        return box

    def define_checkbox(self): # Dark theme
        box = QCheckBox()
        box.setCheckState(self.user_settings['darktheme'])
        box.setDisabled(True)
        return box

    def define_spinbox(self): # Difficulty
        box = QSpinBox()
        box.setToolTip("Create new game after changing difficulty") 
        box.setValue(self.user_settings['difficulty'])
        box.setRange(1,10)

        set_config = lambda: self.update_config('difficulty', box.value())
        
        box.valueChanged.connect(set_config)
        return box

    def define_slider(self): # Board size
        box = QSpinBox()
        box.setToolTip("Create new game after changing board base")
        box.setValue(self.user_settings['board_base'])
        box.setRange(3,10)
        set_config = lambda: self.update_config('board_base', box.value())
         
        box.valueChanged.connect(set_config)
        box.valueChanged.connect(self.parent.updateBase)
        return box

    def get_modules(self):
        return inspect.getmembers(sys.modules[settings.theme.__name__], inspect.isclass)
    
    def update_config(self, name, value):
        print("Updated value:", name, value)
        self.user_settings[name] = value
        self.parent.update()
        