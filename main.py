"""Les interfaces et le code sont assez basiques,
à vous de les améliorer comme bon vous semble"""
############################################
# Importation des bibliothèques nécessaires#
############################################
import sqlite3
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

############################################
# Chemin vers les différents UI            #
############################################
pathSignIn, _ = loadUiType(os.path.join(os.path.dirname(__file__), "sign.ui"))

pathLogin, _ = loadUiType(os.path.join(os.path.dirname(__file__), "login.ui"))

pathHome, _ = loadUiType(os.path.join(os.path.dirname(__file__), "home.ui"))

###########################################
# Connexion à la BDD                      #
###########################################
connection = sqlite3.connect("client.db")
cursor = connection.cursor()

###########################################
#class SignIn                             #
###########################################
class SignIn(QMainWindow, pathSignIn):
    def __init__(self, parent=None):
        super(SignIn, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        QMainWindow.setFixedSize(self, 447,600)
        self.create_table()
        self.btn_sign_in.clicked.connect(self.insertion)
        self.btn_login.clicked.connect(self.show_login)
        surname = self.window().let_surname.text()
        print(self.let_surname.text())

    def show_login(self):
        self.login = Login(self)
        self.hide()
        self.login.show()

    def create_table(self):
        """Code permettant de créer une table et ses champs avec leur type"""
        request = "CREATE TABLE IF NOT EXISTS user(surname TEXT, name TEXT," \
                  " email TEXT, pwd TEXT )"
        cursor.execute(request)

    def insertion(self):
        """Récupération des valeurs se trouvant dans les lineEdit"""
        surname = self.let_surname.text()
        name = self.let_name.text()
        email = self.let_mail.text()
        pwd = self.let_pwd.text()
        """Insertion des valeurs des lineEdit dans la table user de la BDD client"""
        request = "INSERT INTO user VALUES(?,?,?,?)"
        cursor.execute(request, (surname, name, email, pwd))
        connection.commit()
        self.login = Login(self)
        self.hide()
        self.login.show()
##########################################
# Class Login                            #
##########################################
class Login(QMainWindow , pathLogin):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(447, 600)
        self.btn_login.clicked.connect(self.check_login)
        self.lbl_wrong.setText('')

    def check_login(self):
        surname = self.let_surname.text()
        pwd = self.let_pwd.text()
        """Recupère le surname et le password de l'utilisateur dans la BDD 
        si ceux-ci correspondent"""
        request = "SELECT surname, pwd FROM user WHERE surname=surname AND pwd=pwd"
        cursor.execute(request)
        result = cursor.fetchall()

        for row in result:
            if surname == row[0] and pwd == row[1]:
                self.home = Home(self)
                self.hide()
                self.home.show()

            else:
                self.lbl_wrong.setText('Wrong surname or password')

#########################################
# Class Home                            #
#########################################
class Home(QMainWindow, pathHome):
    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(447, 600)
        self.btn_update.clicked.connect(self.update_client)
        self.btn_delete.clicked.connect(self.delete_client)
        request = "SELECT * FROM user"
        result = cursor.execute(request)
        self.tbl_client.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tbl_client.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tbl_client.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def update_client(self):
        """Je n'update que le surname, en prédéfinissant le surname à Chidori, à vous de taper la requête que
        vous voulez selon le résultat que vous attendez. Aussi je n'ai pas utilisé
        d'id, n'empêche que vous puissiez le faire."""
        surname = self.let_surname.text()
        request = "UPDATE user SET surname=? WHERE surname=?"
        cursor.execute(request, ('Chidori', surname))
        connection.commit()

    def delete_client(self):

        surname = self.let_surname.text()
        request = "DELETE FROM user WHERE surname=surname"
        cursor.execute(request)
        connection.commit()

#########################################
# Méthode main                          #
#########################################
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

