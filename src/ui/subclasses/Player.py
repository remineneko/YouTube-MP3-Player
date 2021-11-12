import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from src.main.alter_title import alter_title
from src.ui.generated.ChapterUI import Ui_chapterSelector
from src.ui.generated.PlayScreen import Ui_PlayerWindow

from settings import *

import datetime


class Player(QtWidgets.QMainWindow, Ui_PlayerWindow):

    _DEFAULT_VOLUME = 25

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

        self._previous_row = None

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

        self.queueList.installEventFilter(self)
        self.queueList.itemDoubleClicked.connect(lambda: self.dc_evt(self.queueList.currentIndex()))

        self.volumeSlider.setMaximum(100)

        # set default volume
        self.volumeSlider.setValue(self._DEFAULT_VOLUME)
        self.player.setVolume(self.volumeSlider.value())

        self.player.currentMediaChanged.connect(self._change_media)
        self.player.positionChanged.connect(self._change_pos)

        # self.timeSlider.sliderPressed.connect(self._change_music_pos)
        self.timeSlider.sliderReleased.connect(self._change_music_pos)

        self.volumeSlider.sliderMoved.connect(self._change_volume)

    def set_playlist_pos(self, pos = 0):
        self.current_play_pos = pos
        self.playlist.setCurrentIndex(self.current_play_pos)

    def play(self):
        # if len(self.queueList.selectedItems()) == 1:
        #     self.set_playlist_pos(self.queueList.row(self.queueList.currentItem()))

        if not self.first_song_played:
            self._change_media()
            self.first_song_played = True

        if not self.song_playing:
            self.player.play()
            self.nowPlaying.setText("Now Playing: {}".format(self.storage.now_playing[self.current_play_pos].title))
            self.playButton.setText("Play")
            self.song_playing = True
        else:
            self._pause()

    def _pause(self):
        self.song_playing = False
        self.playButton.setText("Pause")
        self.player.pause()

    def stop(self):
        self.song_playing = False
        self.player.stop()

    def back(self):
        if self.current_play_pos == 0:
            self.player.stop()
            self.song_playing = False
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
            self.shuffleButton.setText("Shuffle ON")
            self.shuffle_state = True
            if self.current_play_state != QMediaPlaylist.CurrentItemOnce:
                self.playlist.setPlaybackMode(QMediaPlaylist.Random)
        else:
            self.shuffle_state = False
            self.shuffleButton.setText("Shuffle")
            self.playlist.setPlaybackMode(self.current_play_state)

    def change_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if self.current_play_pos != self.playlist.mediaCount() - 1:
                self.set_playlist_pos(self.current_play_pos + 1)
                self.player.play()
            elif self.current_play_pos == self.playlist.mediaCount() - 1 and self.current_play_state == QMediaPlaylist.Loop:
                self.set_playlist_pos()
                self.player.play()
            elif self.current_play_state == QMediaPlaylist.CurrentItemOnce:
                self.player.play()
            else:
                self.song_playing = False
                self.player.stop()

    def dc_evt(self, index):
        self.set_playlist_pos(index.row())
        if not self.first_song_played:
            self._change_media()
            self.first_song_played = True
        self.player.play()

    def _change_media(self):
        currently_playing_dur = self.storage.now_playing[self.current_play_pos].duration
        converted_time = str(datetime.timedelta(seconds=currently_playing_dur)).split(".")[0]
        self.nowPlaying.setText("Now Playing: {}".format(self.storage.now_playing[self.current_play_pos].title))
        self.currentTime.setText("0:00:00/{}".format(converted_time))
        segment_length = int(currently_playing_dur)
        self.timeSlider.setMaximum(segment_length)

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

    def _change_volume(self):
        self.player.setVolume(self.volumeSlider.value())

    def eventFilter(self, source, event) -> bool:
        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.queueList):
            song_context_menu = QtWidgets.QMenu()
            chapter_act = song_context_menu.addAction("View chapters")
            # chapter_act.triggered.connect(lambda: self._view_chapters(source.currentItem()))
            choice = song_context_menu.exec_(event.globalPos())
            try:
                item = source.itemAt(event.pos())
            except Exception as e:
                print(f"No item selected {e}")

            if choice == chapter_act:
                self._view_chapters(item)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.queueList:
            self.dc_evt(source.currentIndex())
        return super(QtWidgets.QMainWindow, self).eventFilter(source, event)

    def _pl_song_contextMenu(self, curQueueItem):
        pass

    def _view_chapters(self, cur_item:QtWidgets.QListWidgetItem):
        item_data: MediaMetadata = cur_item.data(QtCore.Qt.UserRole)
        available_chapters = item_data.chapters

        if available_chapters is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("No chapters are available")
            # msg.setInformativeText('No Chapter ')
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            self._chap_dialog = QtWidgets.QDialog()
            self._chap_ui = Ui_chapterSelector()
            self._chap_ui.setupUi(self._chap_dialog)
            self._chap_ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

            # setting up the table
            self._chap_ui.tableWidget.setColumnCount(2)
            self._chap_ui.tableWidget.setRowCount(len(available_chapters))

            for chap_pos in range(len(available_chapters)):
                chap_info = available_chapters[chap_pos]
                chap_start_time = chap_info['start_time']
                chap_title = chap_info['title']
                start_time = str(datetime.timedelta(seconds=chap_start_time)).split(".")[0]
                time_table_wdgt = QtWidgets.QTableWidgetItem(start_time)
                time_table_wdgt.setData(QtCore.Qt.UserRole, chap_start_time)
                self._chap_ui.tableWidget.setItem(chap_pos, 0, time_table_wdgt)
                self._chap_ui.tableWidget.setItem(chap_pos, 1, QtWidgets.QTableWidgetItem(chap_title))

            self._chap_ui.playButton.clicked.connect(lambda: self._play_chapter(self._chap_ui.tableWidget.selectedItems(), cur_item, self._chap_dialog))
            self._chap_ui.tableWidget.itemDoubleClicked.connect(lambda: self._play_chapter(self._chap_ui.tableWidget.selectedItems(), cur_item, self._chap_dialog))
            self._chap_dialog.exec_()

    def _play_chapter(self, selected_chapter, queueItem, dialog):
        dialog.close()
        if len(selected_chapter) == 0:
            pass
        else:
            cur_media_metadata = queueItem.data(QtCore.Qt.UserRole)
            cur_media_duration = cur_media_metadata.duration
            converted_time = str(datetime.timedelta(seconds=cur_media_duration)).split(".")[0]
            set_time = selected_chapter[0].data(QtCore.Qt.UserRole)
            music_cur_pos = set_time * 1000
            self.player.setPosition(music_cur_pos)
            converted_pos = str(datetime.timedelta(seconds=(self.player.position() / 1000))).split(".")[0]
            self.currentTime.setText('{}/{}'.format(converted_pos, converted_time))
            self.player.play()
            self.song_playing = True











    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.player.stop()
