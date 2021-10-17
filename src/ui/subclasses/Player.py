from PyQt5 import QtWidgets, QtGui, QtCore

from src.main.storage import AppStorage
from src.ui.generated.PlayScreen import Ui_PlayerWindow


class Player(QtWidgets.QMainWindow, Ui_PlayerWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(Player, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage
        try:
            self.queueList.addItems([i['title'] for i in self.storage.now_playing])
        except Exception as e:
            print(e)



