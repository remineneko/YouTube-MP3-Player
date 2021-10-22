__author__ = "Hoang Tran"
__version__ = '1.0'

from PyQt5 import QtCore
from settings import *
from src.ui.subclasses import MainUI
from src.main.storage import AppStorage
from src.main.config import setup_config
from PyQt5 import QtWidgets, QtGui
import sys

from queue import Queue


class WriteStream(object):
    def __init__(self, q: Queue):
        self.queue = q

    def write(self, txt):
        self.queue.put(txt)

    def flush(self):
        self.queue.empty()


class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)


def main():
    # Main. Finally. I suppose we can end this program here.

    # This storage will (hypothetically) carry data through windows.

    new_storage = AppStorage()

    # Storage is there.

    # this app has dedicated data folder for more app data
    data_dir = os.path.join(ROOT_FOLDER, 'data')
    try:
        os.mkdir(data_dir, mode=0o777)
    except FileExistsError:
        pass

    music_dir = os.path.join(data_dir, 'now_playing')
    try:
        os.mkdir(music_dir, mode=0o777)
    except FileExistsError:
        pass

    # playlist
    playlist_dir = os.path.join(data_dir, 'SavedPlaylists')
    try:
        os.mkdir(playlist_dir, mode = 0o777)
    except FileExistsError:
        pass

    output_queue = Queue()
    sys.stdout = WriteStream(output_queue)


    # this app has config
    # setup config
    setup_config()

    # Now, Main Window should be loaded now.
    # And now we load the window.
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Benchmark and Stress")
    # app.setWindowIcon(QtGui.QIcon(YANFEI_SMUG))
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow(new_storage)
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    mw = MainUI.MainMenu(new_storage)
    mw.show()

    output_thread = QtCore.QThread()
    output_receiver = MyReceiver(output_queue)
    output_receiver.mysignal.connect(mw.tbOutput)
    output_receiver.moveToThread(output_thread)
    output_thread.started.connect(output_receiver.run)
    output_thread.start()

    app.exec_()

if __name__ == "__main__":
    main()