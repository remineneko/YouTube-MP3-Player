# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\remin\PycharmProjects\yt_mp3_player\YouTube-MP3-Player\assets\AddSongs.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(351, 184)
        self.linksEdit = QtWidgets.QLineEdit(Dialog)
        self.linksEdit.setGeometry(QtCore.QRect(10, 10, 331, 41))
        self.linksEdit.setObjectName("linksEdit")
        self.addSongButton = QtWidgets.QPushButton(Dialog)
        self.addSongButton.setGeometry(QtCore.QRect(10, 60, 331, 31))
        self.addSongButton.setObjectName("addSongButton")
        self.searchButton = QtWidgets.QPushButton(Dialog)
        self.searchButton.setGeometry(QtCore.QRect(10, 100, 331, 31))
        self.searchButton.setObjectName("searchButton")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 140, 331, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Songs"))
        self.addSongButton.setText(_translate("Dialog", "Add Songs"))
        self.searchButton.setText(_translate("Dialog", "Search"))
        self.pushButton.setText(_translate("Dialog", "Add Playlist Content"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
