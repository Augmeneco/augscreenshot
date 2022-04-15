#!/usr/bin/python3

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QSystemTrayIcon
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QObject

import mainwindow, sys, os, time
from pathlib import Path

class PopupHandler(QObject):
    updatePopup = pyqtSignal()
    exitProg = pyqtSignal()

    def start(self):
        while True:
            time.sleep(1)
            value = open('/tmp/augscreen','r').read()
            if value == 'screened\n': 
                self.updatePopup.emit()

            if value == 'closed\n': 
                self.exitProg.emit()
        

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.radioButton_4.clicked.connect(self.rButtonC)
        self.radioButton_5.clicked.connect(self.rButtonSID)

        self.pushButton.clicked.connect(self.launchScreenshoter)
        self.pushButton_2.clicked.connect(self.exitProg)

        self.popupThread = QThread()
        self.popupHandler = PopupHandler()

        self.popupHandler.moveToThread(self.popupThread)
        self.popupThread.started.connect(self.popupHandler.start)

        self.popupHandler.updatePopup.connect(self.launchScreenshoter)
        self.popupHandler.exitProg.connect(self.exitProg)

    def launchScreenshoter(self):
        self.popupThread.exit()

        cmd = 'sleep {};grimshot '.format(self.lineEdit.text())

        if self.radioButton_4.isChecked():
            cmd += 'copy '
        else:
            cmd += 'save '

        cmd += 'screen'

        cmd += '; echo screened > /tmp/augscreen'

        os.system('echo "{}" > /tmp/augscreenevent.sh; echo "" > /tmp/augscreen;notify-send.sh -o "Screenshot: bash /tmp/augscreenevent.sh" -l "echo closed > /tmp/augscreen" AugScreenshot'.format(cmd))
        self.popupThread.start()

    def exitProg(self):
        self.popupThread.exit()
        self.close()

    def rButtonC(self):
        self.radioButton_5.setChecked(False)

    def rButtonSID(self):
        self.radioButton_4.setChecked(False)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
