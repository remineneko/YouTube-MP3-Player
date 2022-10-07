import datetime
import re
import copy
from PyQt5 import QtWidgets, QtGui, QtCore

from src.main.media_metadata import MediaMetadata
from src.ui.generated import MainScreen, PlayOptions, AddSongs, SettingsUI, SearchOptionsUI, InfoWindow, InfoDialog
from src.ui.generated.SmallMetadata import Ui_Metadata
from src.ui.subclasses import Player, SearchSongs

from src.main.load_url import LoadURL, LoadError
from src.main.storage import AppStorage
from src.main.cur_playlist_data import Playlist
from src.main.download_music import download_music
from src.main.link_verification import is_valid_link
from src.main.exceptions import *

import shutil, sys, time


class MainMenu(QtWidgets.QMainWindow, MainScreen.Ui_MainWindow):

    def __init__(self, storage: AppStorage, parent = None):
        super(MainMenu,self).__init__(parent)
        self.storage = storage
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.player_active = False

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(
            lambda: self._show_metadata(data=self.listWidget.currentItem().data(QtCore.Qt.UserRole))
        )
        self.LoadButton.clicked.connect(lambda: self.url_loading(self.linkInput.text()))
        self.playButton.clicked.connect(self.playMusic)
        self.saveButton.clicked.connect(self.savePlaylist)
        self.pushButton.clicked.connect(lambda: self.loadPlaylist(True))

        self.addButton.clicked.connect(self.addSong)
        self.removeButton.clicked.connect(self.removeSong)

        self.settingsButton.clicked.connect(self.setting)

        self._cur_titles_shown = []

        self._output_UI = QtWidgets.QMainWindow()
        self._output_window = InfoWindow.Ui_MainWindow()
        self._output_window.setupUi(self._output_UI)

        self._output_dialog_UI = QtWidgets.QDialog()
        self._output_dialog = InfoDialog.Ui_InfoDialog()
        self._output_dialog.setupUi(self._output_dialog_UI)

    def tbOutput(self, txt):
        self._output_window.outputPrinter.append(txt)
        QtGui.QGuiApplication.processEvents()

    def url_loading(self, input_url):
        if not is_valid_link(input_url, "youtube") and not is_valid_link(input_url, "bilibili"):
            QtWidgets.QMessageBox.warning(self.LoadButton,'Warning','Please put in a proper YouTube/Bilibili video/playlist url')
        else:
            self._output_window.outputPrinter.clear()
            self._output_UI.show()
            try:
                self.load_worker = LoadWorker(input_url, self.storage)
                self.load_worker.finished.connect(self._update_view)
            except LoadError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Failed to load media from the provided URL")
                # msg.setInformativeText('No Chapter ')
                msg.setWindowTitle("Warning")
                msg.exec_()
            self.load_worker.start()

    def _update_view(self):
        try:
            self._output_UI.close()
        except:
            pass
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
        self._output_window.outputPrinter.clear()
        self._output_UI.show()
        self.download_worker = DownloadWorker(self.storage)
        self.download_worker.finished.connect(self._open_playUI)
        self.download_worker.start()

    def _open_playUI(self):
        try:
            self._output_UI.close()
        except:
            pass
        if len(self.storage.vid_info) == 0:
            QtWidgets.QMessageBox.warning(self.playButton, 'Warning',
                                          'Please load the metadata before proceeding to play')
        else:
            try:
                if self.play_music_UI.isVisible():
                    QtWidgets.QMessageBox.warning(self.playButton, 'Warning',
                                          'Another instance of the player is running. Please close it.')
                else:
                    self.play_music_UI = Player.Player(self.storage)
                    self.play_music_UI.show()
            except Exception as e:
                self.play_music_UI = Player.Player(self.storage)
                self.play_music_UI.show()

    def _play_selected(self, dialog: QtWidgets.QDialog, chosen_songs):
        to_add = [i.data(QtCore.Qt.UserRole) for i in chosen_songs]
        self.storage.now_playing.extend(to_add)
        dialog.close()

    def _play_all(self, dialog: QtWidgets.QDialog):
        self.storage.now_playing = copy.deepcopy(self.storage.vid_info)
        dialog.close()

    def savePlaylist(self):
        if len(self.storage.vid_info) == 0:
            QtWidgets.QMessageBox.warning(self.saveButton, 'Warning',
                                          'Please load at least a song before saving')
        else:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save playlist information",
                self.storage.get_user_playlist_path_choice(),
                "JSON (*.json)",
            )
            if len(file_path) != 0:
                Playlist(self.storage.vid_info).save(file_path)

    def loadPlaylist(self, overwriteAll = True):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Load playlist information",
            self.storage.get_user_playlist_path_choice(),
            "JSON (*.json)"
        )
        if len(file_path) != 0:
            self._output_window.outputPrinter.clear()
            self._output_UI.show()
            self.load_saved_worker = LoadSavedPlaylistWorker(self.storage, file_path, overwriteAll)
            self.load_saved_worker.finished.connect(self._update_view)
            self.load_saved_worker.start()

    def addSong(self):
        self.add_song_ui = QtWidgets.QDialog()
        self.add_song_popup = AddSongs.Ui_Dialog()
        self.add_song_popup.setupUi(self.add_song_ui)
        self.add_song_popup.addSongButton.clicked.connect(lambda: self._add_songs(self.add_song_popup.linksEdit.text()))
        self.add_song_popup.searchButton.clicked.connect(self._search_songs)
        self.add_song_popup.pushButton.clicked.connect(lambda: self.loadPlaylist(False))
        self.add_song_ui.exec_()

    def _add_songs(self, content):
        content_list = content.split(";")
        for c in content_list:
            stripped_content = c.replace(" ", "")
            if len(stripped_content) != 0:
                self._worker = AddWorker(stripped_content, self.storage)
                self._worker.finished.connect(self._update_view)
                self._worker.start()
        self.add_song_ui.close()

    def removeSong(self):
        selectedItems = self.listWidget.selectedItems()
        if len(selectedItems) == 0:
            QtWidgets.QMessageBox.warning(self.removeButton, 'Warning',
                                          'Please choose at least a song to be removed')
        else:
            for item in selectedItems:
                self.listWidget.takeItem(self.listWidget.row(item))
                self.storage.remove_entry(item.data(QtCore.Qt.UserRole))
            self._update_view()

    def setting(self):
        self.settings_ui = QtWidgets.QDialog()
        self.settings_dialog = SettingsUI.Ui_Dialog()
        self.settings_dialog.setupUi(self.settings_ui)

        self.settings_dialog.playlistPathEdit.setText(self.storage.get_user_playlist_path_choice())
        self.settings_dialog.musicPathEdit.setText(self.storage.get_user_music_path_choice())
        self.settings_dialog.isFlushing.setChecked(self.storage.get_user_flush_choice())

        self.settings_dialog.plBrowse.clicked.connect(self._plBrowse)
        self.settings_dialog.musicBrowse.clicked.connect(self._mBrowse)
        self.settings_dialog.confirmOptions.accepted.connect(self._modify_config)

        self.settings_ui.exec_()

    def _plBrowse(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if len(folder_path) != 0:
            self.settings_dialog.playlistPathEdit.setText(folder_path)

    def _mBrowse(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if len(folder_path) != 0:
            self.settings_dialog.musicPathEdit.setText(folder_path)

    def _modify_config(self):
        self.storage.modify_pl_config(self.settings_dialog.playlistPathEdit.text())
        self.storage.modify_music_config(self.settings_dialog.musicPathEdit.text())
        self.storage.modify_flush_config(self.settings_dialog.isFlushing.isChecked())

    def _search_songs(self):
        self.search_option_ui = QtWidgets.QDialog()
        self.search_option_popup = SearchOptionsUI.Ui_SearchOptionsUI()
        self.search_option_popup.setupUi(self.search_option_ui)
        self.search_option_popup.YTSearch.clicked.connect(lambda: self._search("YouTube"))
        self.search_option_popup.pushButton_2.clicked.connect(lambda: self._search("Bilibili"))
        self.search_option_ui.exec_()

    def _search(self, option):
        self.search_option_ui.close()
        self.add_song_ui.close()
        self.search_main_ui = SearchSongs.Searcher(self.storage, option)
        self.search_main_ui.searchButton.clicked.connect(lambda: self.search_main_ui.search(self.search_main_ui.queryEdit.text(), self._output_window, self._output_UI))
        self.search_main_ui.addButton.clicked.connect(self._add_results)
        self.search_main_ui.show()

    def _add_results(self):
        all_results = self.search_main_ui.searchResultBox.selectedItems()
        self.storage.add_entry([i.data(QtCore.Qt.UserRole) for i in all_results])
        self.search_main_ui.close()
        self._update_view()

    def _show_metadata(self, data:MediaMetadata):
        self.meta_widget = QtWidgets.QWidget()
        self.meta_wid_ui = Ui_Metadata()
        self.meta_wid_ui.setupUi(self.meta_widget)
        self.meta_wid_ui.titleLabel.setText(data.title)
        converted_time = str(datetime.timedelta(seconds=data.duration)).split(".")[0]
        self.meta_wid_ui.timeLabel.setText(converted_time)
        self.meta_wid_ui.urlLabel.setText(data.original_url)
        self.meta_wid_ui.uploaderLabel.setText(data.uploader)
        self.meta_widget.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.storage.get_user_flush_choice():
            folder = self.storage.get_user_music_path_choice()
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception:
                    print('Failed to delete %s.' % (file_path))

        a0.accept()
        sys.exit(0)


class AddWorker(QtCore.QThread):
    def __init__(self, url, storage:AppStorage):
        super(AddWorker, self).__init__()
        self._url = url
        self._storage = storage

    def run(self):
        data = LoadURL(self._url).obtained_data
        self._storage.add_entry(data)


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
        try:
            download_music(self.storage)
        except Exception as e:
            print(e)


class LoadSavedPlaylistWorker(QtCore.QThread):
    def __init__(self, storage: AppStorage, filePath:str, overwriteAll = True):
        super(LoadSavedPlaylistWorker, self).__init__()

        self.storage = storage
        self.fp = filePath
        self.role = overwriteAll

    def run(self):
        if self.role:
            try:
                self.storage.vid_info = copy.deepcopy(Playlist().load(self.fp))
            except LoadError as e:
                create_new_msg_box(str(e), "Warning")
            except IncorrectJSONFileError:
                create_new_msg_box(f"The JSON file provided is not in correct format. Please try with a different file", "Warning")
            except IncorrectFileTypeError:
                create_new_msg_box("The provided file is not JSON. Please try with a different file", "Warning")
        else:
            self.storage.add_entry(copy.deepcopy(Playlist().load(self.fp)))


def create_new_msg_box(send_msg:str, win_title:str):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(send_msg)
    # msg.setInformativeText('No Chapter ')
    msg.setWindowTitle(win_title)
    time.sleep(2)
    msg.exec_()


if __name__ == "__main__":
    new_storage = AppStorage()
    from settings import *
    from src.main.config import setup_config
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

    setup_config()

    app = QtWidgets.QApplication(sys.argv)
    ui = MainMenu(new_storage)
    ui.show()
    sys.exit(app.exec_())

