import inspect
import sys

from PyQt5.QtCore import QRect, QSettings, QSize, Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                             QGridLayout, QGroupBox, QLabel, QPushButton,
                             QSlider, QSpinBox)

#from settings.config import user_settings, default_settings
#import settings.theme

class settingGUI(QDialog):
    def __init__(self, parent=None):
        super(settingGUI, self).__init__(parent)
        self.parent = parent
        self.modules = [item for item in self.get_modules()]
        self.user_settings = parent.user_settings
        self.configureUI(self)

    def configureUI(self, Dialog):
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle("Settings") 

        self.horizontalGroupBox = QGroupBox("Grid")
        self.layout = QGridLayout()
        layout = self.layout

        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 5)
        
        self.grid_setup = (
            (QLabel("Theme:"), self.theme_handler()),
            (QLabel("Dark Theme:"), self.darktheme_handler()),
            (QLabel("Difficulty:"), self.difficulty_handler()),
            (QLabel("board_base"),self.base_handler()),
            ('', self.restore_handler()),
            ('',self.accept_handler()),
            (QLabel("Create a new game in order for difficulty and board base to update"), '')
        )

        for index,item in enumerate(self.grid_setup):
            if not item[0] == '':
                layout.addWidget(item[0],index,0)
            if not item[1] == '':   
                layout.addWidget(item[1],index,1)
     
        self.horizontalGroupBox.setLayout(layout)
        self.setLayout(layout)


    def update_settings(self):
        action_table = {
            "theme": (lambda obj: obj.setCurrentIndex(self.modules.index(self.user_settings['theme']))),
            "darktheme": (lambda obj: obj.setCheckState(self.user_settings['darktheme'])),
            "difficulty": (lambda obj: obj.setValue(self.user_settings['difficulty'])),
            "board_base": (lambda obj: obj.setValue(self.user_settings['board_base'])),
        }   
        for value in self.grid_setup:
            
            if not isinstance(value[1], str) and value[1].objectName() in action_table:
                action_table[value[1].objectName()](value[1])

    
    def theme_handler(self): # Theme setting
        """
        Add combobox for menu that handles theme setting
        """
        box = QComboBox()
        box.setObjectName("theme")
        box.addItems(self.modules)
        
        box.setCurrentIndex(self.modules.index(self.user_settings['theme']))
        
        set_config = lambda: self.update_config('theme', self.modules[box.currentIndex()]) 
        box.currentIndexChanged.connect(set_config)
        return box

    def darktheme_handler(self): # Dark theme
        """
        Add checkbox for menu that handles dark theme
        """
        box = QCheckBox()
        box.setObjectName("darktheme")
        box.setCheckState(self.user_settings['darktheme'])
        box.setDisabled(True)
        return box

    def difficulty_handler(self): # Difficulty
        """
        Add spinbox for menu that handles Difficulty of the board
        """
        box = QSpinBox()
        box.setObjectName("difficulty")
        box.setToolTip("Create new game after changing difficulty") 
        box.setValue(self.user_settings['difficulty'])
        box.setRange(1,10) # TODO: ADD to config

        set_config = lambda: self.update_config('difficulty', box.value())
        
        box.valueChanged.connect(set_config)
        return box

    def base_handler(self): # Board size
        """
        Add slider for menu
        """
        box = QSpinBox()
        box.setObjectName("board_base")
        box.setToolTip("Create new game after changing board base")
        box.setValue(self.user_settings['board_base'])
        box.setRange(3,10) # TODO: ADD to config
        set_config = lambda: self.update_config('board_base', box.value())
         
        box.valueChanged.connect(set_config)
        return box

    def restore_handler(self):
        box = QPushButton()
        box.setToolTip("Restore to default settings")
        box.setText("Reset config")
        box.setFixedWidth(100)
        box.clicked.connect(self.restore_config)
        
        return box
    def accept_handler(self):
        box = QPushButton()
        box.setToolTip("Accept changes")
        box.setText("Accept changes")
        box.setFixedWidth(150)
        box.clicked.connect(self.parent.newGame)
        box.clicked.connect(self.update_settings)
        return box

    def restore_config(self):
        # In order to not override address
        for key in self.user_settings.keys():
            self.user_settings[key] = self.parent.configs['users'].data['default_settings'][key]
        
        self.update_settings()


    def get_modules(self):
        return [p for p in self.parent.themes]
        
    def update_config(self, name, value):
        self.user_settings[name] = value
        self.parent.update() 
