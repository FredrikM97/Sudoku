from PyQt5.QtCore import QRect, QSettings, QSize, Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                             QGridLayout, QGroupBox, QLabel, QPushButton,
                             QSlider, QSpinBox)

class StatisticsGUI(QDialog):
    def __init__(self,parent=None):
        super(StatisticsGUI, self).__init__(parent)
        self.parent = parent
        self.statistics = parent.user_settings['statistics']
        self.configureUI(self)

    def configureUI(self, dialog):
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle("Statistics")

        self.horizontalGroupBox = QGroupBox("Grid")
        self.layout = QGridLayout()
        layout = self.layout

        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 5)
        
        self.grid_setup = (
            (QLabel("Win:"), QLabel(str(self.statistics['win']))),
            (QLabel("Games:"), QLabel(str(self.statistics['games']))),
            (QLabel("Best time:"), QLabel(str(self.statistics['best_time'])+ " seconds")),
        )

        for index,item in enumerate(self.grid_setup):
            if not item[0] == '':
                layout.addWidget(item[0],index,0)
            if not item[1] == '':   
                layout.addWidget(item[1],index,1)
     
        self.horizontalGroupBox.setLayout(layout)
        self.setLayout(layout) 