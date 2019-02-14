#important bib
import sqlite3
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#path for signin ui file
pathSignIn = loadUiType(os.path.join(os.path.dirname(__file__), "sign.ui"))

#class SignIn
class SignIn(QMainWindow, pathSignIn):
    def __init__(self, parent=None):
        super(SignIn, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        QMainWindow.setFixedSize(self, 447,600)

#main method
def main():
    app = QApplication(sys.argv)
    window = SignIn()
    window.show()
    app.exec()

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        print(e)

