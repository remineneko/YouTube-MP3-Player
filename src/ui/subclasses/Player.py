from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from src.main.alter_title import alter_title
from src.ui.generated.PlayScreen import Ui_PlayerWindow

from settings import *

import datetime


class Player(QtWidgets.QMainWindow, Ui_PlayerWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(Player, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage

        self.first_song_played = False

        self.song_playing = False
        self.stop_state = False

        self.passed_loop_all = False
        self.passed_loop_once = False

        self.shuffle_state = False
        self.current_play_state = QMediaPlaylist.CurrentItemOnce

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

        self.set_playlist_pos()

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.mediaStatusChanged.connect(lambda: self.change_status(QMediaPlayer.MediaStatus))

        self.currentTime.setText("")

        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.backPlayButton.clicked.connect(self.back)
        self.fowardPlayButton.clicked.connect(self.foward)
        self.repeatButton.clicked.connect(self.repeat)
        self.shuffleButton.clicked.connect(self.shuffle)
        self.queueList.itemDoubleClicked.connect(lambda: self.dc_evt(self.queueList.currentIndex()))

        self.player.currentMediaChanged.connect(self._change_media)
        self.player.positionChanged.connect(self._change_pos)

        # self.timeSlider.sliderPressed.connect(self._change_music_pos)
        self.timeSlider.sliderReleased.connect(self._change_music_pos)

    def set_playlist_pos(self, pos = 0):
        self.current_play_pos = pos
        self.playlist.setCurrentIndex(self.current_play_pos)

    def play(self):
        if not self.first_song_played:
            self._change_media()
            self.first_song_played = True

        if not self.song_playing:
            self.player.play()
            self.nowPlaying.setText("Now Playing: {}".format(self.storage.now_playing[self.current_play_pos].title))
            self.song_playing = True
        else:
            self._pause()

    def _pause(self):
        self.song_playing = False
        self.player.pause()

    def stop(self):
        self.song_playing = False
        self.player.stop()

    def back(self):
        if self.current_play_pos == 0:
            self.player.stop()
            self.play()
        else:
            self.set_playlist_pos(self.current_play_pos - 1)
            self.song_playing = False
            self.play()

    def foward(self):
        if self.current_play_pos >= self.playlist.mediaCount() - 1:
            pass
        else:
            self.set_playlist_pos(self.current_play_pos + 1)
            self.song_playing = False
            self.play()

    def repeat(self):
        if not self.passed_loop_all:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.current_play_state = QMediaPlaylist.Loop
            self.repeatButton.setText("Repeat All")
            self.passed_loop_all = True
        elif not self.passed_loop_once:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.current_play_state = QMediaPlaylist.CurrentItemInLoop
            self.repeatButton.setText("Repeat One")
            self.passed_loop_once = True
        elif self.passed_loop_all and self.passed_loop_once:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
            self.current_play_state = QMediaPlaylist.CurrentItemOnce
            self.repeatButton.setText("Repeat")
            self.passed_loop_once = False
            self.passed_loop_all = False

    def shuffle(self):
        if not self.shuffle_state:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            self.shuffle_state = True
        else:
            self.shuffle_state = False
            self.playlist.setPlaybackMode(self.current_play_state)

    def change_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if self.current_play_pos != self.playlist.mediaCount() - 1:
                self.set_playlist_pos(self.current_play_pos + 1)
                self.player.play()
            elif self.current_play_pos == self.playlist.mediaCount() - 1 and self.current_play_state == QMediaPlaylist.Loop:
                self.set_playlist_pos()
                self.player.play()
            else:
                self.player.stop()

    def dc_evt(self, index):
        self.set_playlist_pos(index.row())
        self._change_media()
        self.player.play()

    def _change_media(self):
        try:
            currently_playing_dur = self.storage.now_playing[self.current_play_pos].duration
            converted_time = str(datetime.timedelta(seconds=currently_playing_dur)).split(".")[0]
            self.nowPlaying.setText("Now Playing: {}".format(self.storage.now_playing[self.current_play_pos].title))
            self.currentTime.setText("0:00:00/{}".format(converted_time))
            segment_length = int(currently_playing_dur)
            self.timeSlider.setMaximum(segment_length)
        except Exception as e:
            print(e)

    def _change_pos(self):
        currently_playing_dur = self.storage.now_playing[self.current_play_pos].duration
        converted_time = str(datetime.timedelta(seconds=currently_playing_dur)).split(".")[0]
        cur_pos = int(self.player.position() / 1000)
        self.timeSlider.setValue(cur_pos)
        converted_pos = str(datetime.timedelta(seconds=(self.player.position()/1000))).split(".")[0]
        self.currentTime.setText('{}/{}'.format(converted_pos,converted_time))

    def _change_music_pos(self):
        cur_pos = self.timeSlider.value()
        currently_playing_dur = self.storage.now_playing[self.current_play_pos].duration
        converted_time = str(datetime.timedelta(seconds=currently_playing_dur)).split(".")[0]
        music_cur_pos = cur_pos * 1000
        self.player.setPosition(music_cur_pos)
        converted_pos = str(datetime.timedelta(seconds=(self.player.position() / 1000))).split(".")[0]
        self.currentTime.setText('{}/{}'.format(converted_pos, converted_time))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.player.stop()
