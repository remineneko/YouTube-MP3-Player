from PyQt5 import QtWidgets, QtGui
from src.ui.generated import MainScreen


class MainMenu(QtWidgets.QMainWindow, MainScreen.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainMenu,self).__init__(parent)