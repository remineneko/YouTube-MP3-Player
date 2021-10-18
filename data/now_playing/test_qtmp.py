from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
import sys

app = QtGui.QGuiApplication(sys.argv)
player = QtMultimedia.QMediaPlayer()
sound = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile("『Fuwa Fuwa Time』by Pastel_Palettes.mp3"))
player.setMedia(sound)
player.setVolume(100)
player.play()
sys.exit(app.exec_())
