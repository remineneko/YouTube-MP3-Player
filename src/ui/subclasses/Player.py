from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl, QCoreApplication
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from src.main.storage import AppStorage
from src.ui.generated.PlayScreen import Ui_PlayerWindow

from settings import *


class Player(QtWidgets.QMainWindow, Ui_PlayerWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(Player, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage

        self.queueList.addItems([i['title'] for i in self.storage.now_playing])
        self.player = QMediaPlayer(self)
        self.playButton.clicked.connect(self.play)

    def play(self):
        selected_song_for_play = self.queueList.selectedItems()

        # if no song is chosen to be played first, defaults the first song to be played.

        if len(selected_song_for_play) == 0:
            self._setup_play(self.storage.now_playing[0])
        elif len(selected_song_for_play) >= 1:
            chosen_song = [i for i in self.storage.now_playing if i['title'] in selected_song_for_play]
            for song in chosen_song:
                self._setup_play(song)

    def _setup_play(self, song_metadata):
        song_name = song_metadata['title']
        location = os.path.join(MUSIC_FOLDER, '{}.mp3'.format(song_name))
        url = QUrl.fromLocalFile(location)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.nowPlaying.setText("Now playing: {}".format(song_name))
        self.player.setVolume(50)
        self.player.play()

