from PyQt5 import QtWidgets, QtGui, QtCore

from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from src.main.search import SearchVideos
from src.ui.generated.SearchUI import Ui_SearchWindow
from src.ui.generated.SmallMetadata import Ui_Metadata


import datetime


class Searcher(QtWidgets.QMainWindow, Ui_SearchWindow):
    def __init__(self, storage:AppStorage, search_website, parent = None):
        super(Searcher, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage
        self._search_website = search_website
        self._search_inst = SearchVideos(self.storage, self._search_website)
        self.searchButton.clicked.connect(lambda: self.search(self.queryEdit.text()))
        self.searchResultBox.itemDoubleClicked.connect(lambda: self._show_metadata(data = self.searchResultBox.currentItem().data(QtCore.Qt.UserRole)))
        self.searchResultBox.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def search(self, query):
        self.search_worker = SearchWorker(self.storage, self._search_inst, query)
        self.search_worker.finished.connect(self.finished_searching)
        self.search_worker.start()

    def _running_warning(self, worker):
        while worker.running:
            if self.searchButton.clicked:
                QtWidgets.QMessageBox.warning(self.searchButton, 'Warning',
                                              'Please wait for the search to complete')
            elif self.addButton.clicked:
                QtWidgets.QMessageBox.warning(self.addButton, 'Warning',
                                              'Please wait for the search to complete')

    def finished_searching(self):
        self.searchResultBox.clear()
        for r_index in range(len(self.storage.temp_search_storage)):
            item = self.storage.temp_search_storage[r_index]
            self.searchResultBox.addItem(item.title)
            self.searchResultBox.item(r_index).setData(QtCore.Qt.UserRole, item)

    def _show_metadata(self, data:MediaMetadata):
        self.meta_widget = QtWidgets.QWidget()
        self.meta_wid_ui = Ui_Metadata()
        self.meta_wid_ui.setupUi(self.meta_widget)
        self.meta_wid_ui.titleLabel.setText(data.title)
        converted_time = str(datetime.timedelta(seconds=data.duration)).split(".")[0]
        self.meta_wid_ui.timeLabel.setText(converted_time)
        self.meta_wid_ui.urlLabel.setText(data.original_url)
        self.meta_widget.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.search_worker.running:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please wait for the search to complete')
            self.error_dialog.exec_()
        else:
            self.close()


class SearchWorker(QtCore.QThread):
    def __init__(self, storage: AppStorage, search_inst: SearchVideos, query):
        super(SearchWorker, self).__init__()
        self.storage = storage
        self.search_inst = search_inst
        self.query = query
        self.running = True

    def run(self):
        self.storage.get_search_data(self.search_inst.search(self.query))
        self.running = False