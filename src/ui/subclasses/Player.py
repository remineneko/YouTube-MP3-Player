from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

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
        self.pause_state = False

        for now_playing_item_index in range(len(self.storage.now_playing)):
            self.queueList.addItem(self.storage.now_playing[now_playing_item_index].title)
            self.queueList.item(now_playing_item_index).setData(self.storage.now_playing[now_playing_item_index])

        self.player = QMediaPlayer(self)
        self.playButton.clicked.connect(self.play)

    def play(self):
        selected_song_for_play = self.queueList.selectedItems()

        if not self.song_playing:
            if not self.pause_state:
                # if no song is chosen to be played first, defaults the first song to be played.

                if len(selected_song_for_play) == 0:
                    self._setup_play(self.storage.now_playing[0])
                elif len(selected_song_for_play) >= 1:
                    chosen_song = [i.data(QtCore.Qt.UserRole) for i in selected_song_for_play]
                    for song in chosen_song:
                        self._setup_play(song)
            else:
                self.player.play()
                self.pause_state = False

        elif self.song_playing and len(selected_song_for_play) >= 1:
            chosen_song = [i.data(QtCore.Qt.UserRole) for i in selected_song_for_play]
            self._setup_play(chosen_song[0])

        else:
            self._pause()

    def _setup_play(self, song_metadata: MediaMetadata):
        song_name = alter_title(song_metadata.title)
        location = os.path.join(MUSIC_FOLDER, '{}.mp3'.format(song_name))
        url = QUrl.fromLocalFile(location)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.nowPlaying.setText("Now playing: {}".format(song_name))
        self.player.setVolume(50)
        self.song_playing = True
        self.player.play()

    def _pause(self):
        self.song_playing = False
        self.pause_state = True
        self.player.pause()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.player.stop()