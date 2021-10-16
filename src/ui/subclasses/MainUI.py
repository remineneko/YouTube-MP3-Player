from PyQt5 import QtWidgets, QtGui, QtCore
from src.ui.generated import MainScreen
from src.main.storage import AppStorage
from src.main.load_url import LoadURL


class MainMenu(QtWidgets.QMainWindow, MainScreen.Ui_MainWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(MainMenu,self).__init__(parent)
        self.storage = storage
        self.setupUi(self)

        self.LoadButton.clicked.connect(lambda: self.url_loading(self.linkInput.text()))
        self._cur_titles_shown = []

    def url_loading(self, input_url):
        self.load_worker = LoadWorker(input_url, self.storage)
        self.load_worker.finished.connect(self._update_view)
        self.load_worker.start()

    def _update_view(self):
        self.listWidget.clear()
        self.listWidget.addItems([i['title'] for i in self.storage.vid_info])


class LoadWorker(QtCore.QThread):
    def __init__(self, url, storage):
        super(LoadWorker, self).__init__()
        self.url = url
        self.storage = storage

    def run(self):
        LoadURL(self.url, self.storage)

if __name__ == "__main__":
    new_storage = AppStorage()
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainMenu(new_storage)
    ui.show()
    sys.exit(app.exec_())

