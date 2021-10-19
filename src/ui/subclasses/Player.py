from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from src.main.alter_title import alter_title
from src.ui.generated.PlayScreen import Ui_PlayerWindow

from settings import *


class Player(QtWidgets.QMainWindow, Ui_PlayerWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(Player, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage

        self.song_playing = False
        self.stop_state = False

        self.playlist = QMediaPlaylist()
        self.setFixedSize(self.size())

        for now_playing_item_index in range(len(self.storage.now_playing)):
            cur_item = self.storage.now_playing[now_playing_item_index]
            self.queueList.addItem(cur_item.title)
            self.queueList.item(now_playing_item_index).setData(QtCore.Qt.UserRole, cur_item)
            song_name = alter_title(cur_item.title)
            location = os.path.join(MUSIC_FOLDER, '{}.mp3'.format(song_name))
            url = QUrl.fromLocalFile(location)
            content = QMediaContent(url)
            self.playlist.addMedia(content)

        self.current_play_pos = 0
        self.playlist.setCurrentIndex(self.current_play_pos)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.playButton.clicked.connect(self.play)

    def play(self):
        if not self.song_playing:
            self.player.play()
            self.song_playing = True
        else:
            self._pause()

    def _pause(self):
        self.song_playing = False
        self.player.pause()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.player.stop()