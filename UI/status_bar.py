from PyQt5.QtWidgets import QAction
#from UI.gui import display_popup, newGame, showSolution, restartGame, showSettings,checkSolution

class Status_bar(object):
    def status_action(self, name, shortCut, statusTip, obj,trigger):
            """
            Factorised creation of actions 
            """
            action = QAction(name, obj) 
            action.setShortcut(shortCut)
            action.setStatusTip(statusTip)
            if not trigger == None:
                action.triggered.connect(trigger)
            return action

    def status_bar(self, dialog=None) -> None:
        """
        Add statusbar to the menu
        """
        actions = [
            (0,"New game", "Ctrl+N", "Start new game",dialog, dialog.newGame),
            (0,"Reset game", "Ctrl+R", "Reset game", dialog,dialog.restartGame),
            (0,"Correct game", "Ctrl+C", "Check if your board is correct",dialog, dialog.checkSolution),
            (0,"Exit", "Ctrl+Q", "Exit the App",dialog, dialog.quit),
            (1,"Settings", "Ctrl+E", "Show settings", dialog,dialog.openSettings),
            (1,"Solution", "Ctrl+S", "Get the solution",dialog, dialog.showSolution),
            (1,"Statistics", "Ctrl+k", "Get game statistics",dialog, dialog.openStatistics),
            (2,"Info", "Ctrl+I", "Show info",dialog, lambda titl="Information", message="Made by https://github.com/FredrikM97": dialog.display_popup(titl, message)),
            
        ]
        int2str = {
            0:'File',
            1:'Edit',
            2:'Info'
        }
        mainMenu = dialog.menuBar()
        dialog.statusBar()
        menu = [mainMenu.addMenu(index) for index in [*int2str.values()]]

        for item in actions:
            menu[item[0]].addAction(self.status_action(*item[1:])) 
        