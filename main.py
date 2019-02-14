#importation des bibliothèques nécessaires
import sqlite3
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#chemin du fichier qui contient l'interface sign in
pathSignIn, _ = loadUiType(os.path.join(os.path.dirname(__file__), "sign.ui"))
#connexion à la base de données
connexion = sqlite3.connect("client.db")
c = connexion.cursor()

#class SignIn
class SignIn(QMainWindow, pathSignIn):
    def __init__(self, parent=None):
        super(SignIn, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        QMainWindow.setFixedSize(self, 447,600)
        #execution de la méthode create_table
        self.create_table()

    def create_table(self):
        """Code permettant de créer une table et ses champs"""
        c.execute("CREATE TABLE IF NOT EXISTS user(surname TEXT, name TEXT, email TEXT, pwd TEXT )")

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

