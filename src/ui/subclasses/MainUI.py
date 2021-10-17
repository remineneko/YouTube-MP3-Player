import re
import copy
from PyQt5 import QtWidgets, QtGui, QtCore

from src.ui.generated import MainScreen, PlayOptions
from src.ui.subclasses import Player

from src.main.load_url import LoadURL
from src.main.storage import AppStorage


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
        self.listWidget.addItems([i['title'] for i in self.storage.vid_info])

    def playMusic(self):
        all_songs_chosen = self.listWidget.selectedItems()
        if len(all_songs_chosen) == 0:
            self.storage.now_playing = copy.deepcopy(self.storage.vid_info)
        elif len(all_songs_chosen) == 1:
            # this is very unoptimized
            # note to self: think of a different way to implement this
            to_add = [i for i in self.storage.vid_info if i['title'] == all_songs_chosen[0].text()]
            self.storage.now_playing = copy.deepcopy(to_add)
        else:
            self.popup_ui = QtWidgets.QDialog()
            self.play_popup = PlayOptions.Ui_PlayOptions()
            self.play_popup.setupUi(self.popup_ui)
            self.play_popup.playSelected.clicked.connect(lambda: self._play_selected(self.popup_ui, all_songs_chosen))
            self.play_popup.playAllButton.clicked.connect(lambda: self._play_all(self.popup_ui))
            self.popup_ui.exec_()

        # open the play UI
        self.play_music_UI = Player.Player(self.storage)
        self.play_music_UI.show()

    def _play_selected(self, dialog: QtWidgets.QDialog, chosen_songs):
        to_add = [i for i in self.storage.vid_info if i['title'] in [t.text() for t in chosen_songs]]
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

if __name__ == "__main__":
    new_storage = AppStorage()
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainMenu(new_storage)
    ui.show()
    sys.exit(app.exec_())

