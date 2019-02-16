"""Les interfaces et le code sont assez basiques, à vous de les améliorer à votre guise"""
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
#chemin du fichier qui contient l'interface login
pathLogin, _ = loadUiType(os.path.join(os.path.dirname(__file__), "login.ui"))
#chemin du fichier qui contient l'interface home
pathHome, _ = loadUiType(os.path.join(os.path.dirname(__file__), "home.ui"))

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
        self.btn_sign_in.clicked.connect(self.insertion)
        #self.btn_login.clicked.connect(self.show_login)
        surname = self.window().let_surname.text()
        print(self.let_surname.text())

    def show_login(self):
        login = Login(self)

    def create_table(self):
        """Code permettant de créer une table et ses champs avec leur type"""
        c.execute("CREATE TABLE IF NOT EXISTS user(surname TEXT, name TEXT, email TEXT, pwd TEXT )")

    def insertion(self):
        #recupération des valeurs se trouvant dans les lineEdit
        surname = self.let_surname.text()
        name = self.let_name.text()
        email = self.let_mail.text()
        pwd = self.let_pwd.text()
        #insertion des valeurs des lineEdit dans la table user de la BDD client
        c.execute("INSERT INTO user VALUES(?,?,?,?)", (surname, name, email, pwd))
        connexion.commit()
        self.login = Login(self)
        self.hide()
        self.login.show()
        #c.close()
        #connexion.close()

class Login(QMainWindow , pathLogin):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(447, 600)
        self.btn_login.clicked.connect(self.check_login)

    def check_login(self):
        surname = self.let_surname.text()
        pwd = self.let_pwd.text()
        #Recupère le surname et le password de l'utilisateur dans la BDD si ceux-ci correspondent
        c.execute("SELECT surname, pwd FROM user WHERE surname=surname AND pwd=pwd")
        data = c.fetchall()

        for row in data:
            if surname == row[0] and pwd == row[1]:
                self.home = Home(self)
                self.hide()
                self.home.show()

            else:
                print("incohérence")

class Home(QMainWindow, pathHome):
    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(447, 600)


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

