import re
import copy
from PyQt5 import QtWidgets, QtGui, QtCore

from src.ui.generated import MainScreen, PlayOptions
from src.ui.subclasses import Player

from src.main.load_url import LoadURL
from src.main.storage import AppStorage
from src.main.download_music import download_music

from settings import *


class MainMenu(QtWidgets.QMainWindow, MainScreen.Ui_MainWindow):

    def __init__(self, storage: AppStorage, parent = None):
        super(MainMenu,self).__init__(parent)
        self.storage = storage
        self.setupUi(self)

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.LoadButton.clicked.connect(lambda: self.url_loading(self.linkInput.text()))
        self.playButton.clicked.connect(self.playMusic)
        self._cur_titles_shown = []

    @staticmethod
    def is_valid_youtube_url(given_url):
        return bool(re.search(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', given_url))

    def url_loading(self, input_url):
        if not self.is_valid_youtube_url(input_url): # bilibili support will come later, please wait for it Rem :p
            QtWidgets.QMessageBox.warning(self.LoadButton,'Warning','Please put in a proper YouTube video/playlist url')
        else:
            self.load_worker = LoadWorker(input_url, self.storage)
            self.load_worker.finished.connect(self._update_view)
            self.load_worker.start()

    def _update_view(self):
        self.listWidget.clear()
        for song_metadata_ind in range(len(self.storage.vid_info)):
            self.listWidget.addItem(self.storage.vid_info[song_metadata_ind].title)
            self.listWidget.item(song_metadata_ind).setData(QtCore.Qt.UserRole,self.storage.vid_info[song_metadata_ind])

    def playMusic(self):
        all_songs_chosen = self.listWidget.selectedItems()
        if len(all_songs_chosen) == 0:
            self.storage.now_playing = copy.deepcopy(self.storage.vid_info)
        elif len(all_songs_chosen) == 1:
            to_add = [i.data(QtCore.Qt.UserRole) for i in all_songs_chosen]
            self.storage.now_playing = copy.deepcopy(to_add)
        else:
            self.popup_ui = QtWidgets.QDialog()
            self.play_popup = PlayOptions.Ui_PlayOptions()
            self.play_popup.setupUi(self.popup_ui)
            self.play_popup.playSelected.clicked.connect(lambda: self._play_selected(self.popup_ui, all_songs_chosen))
            self.play_popup.playAllButton.clicked.connect(lambda: self._play_all(self.popup_ui))
            self.popup_ui.exec_()

        # load the songs into a folder first

        self.download_worker = DownloadWorker(self.storage)
        self.download_worker.finished.connect(self._open_playUI)
        self.download_worker.start()

    def _open_playUI(self):
        self.play_music_UI = Player.Player(self.storage)
        self.play_music_UI.show()

    def _play_selected(self, dialog: QtWidgets.QDialog, chosen_songs):
        to_add = [i.data(QtCore.Qt.UserRole) for i in chosen_songs]
        self.storage.now_playing.extend(to_add)
        dialog.close()

    def _play_all(self, dialog: QtWidgets.QDialog):
        self.storage.now_playing = copy.deepcopy(self.storage.vid_info)
        dialog.close()


class LoadWorker(QtCore.QThread):
    def __init__(self, url, storage):
        super(LoadWorker, self).__init__()
        self.url = url
        self.storage = storage

    def run(self):
        LoadURL(self.url, self.storage)


class DownloadWorker(QtCore.QThread):
    def __init__(self, storage):
        super(DownloadWorker, self).__init__()
        self.storage = storage

    def run(self):
        download_music(info_list=self.storage.now_playing)


if __name__ == "__main__":
    new_storage = AppStorage()
    from settings import *
    data_dir = os.path.join(ROOT_FOLDER, 'data')
    try:
        os.mkdir(data_dir, mode= 0o777)
    except FileExistsError:
        pass

    music_dir = os.path.join(data_dir,'now_playing')
    try:
        os.mkdir(music_dir,mode=0o777)
    except FileExistsError:
        pass

    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainMenu(new_storage)
    ui.show()
    sys.exit(app.exec_())

