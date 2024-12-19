from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtCore


class Authentication:
    def __init__(self, view):
        self.view = view
        self.is_auth = False
        self.connect_slots()
        self.password = '3113'

    def connect_slots(self):
        self.view.tabWidget.currentChanged.connect(self.check_password_tabWidget)
        self.view.listWidget.currentRowChanged.connect(self.check_password_listWidget)
        self.view.Control_tabWidget.currentChanged.connect(self.check_password_Control_tabWidget)

    def check_password_Control_tabWidget(self, index):
        if (index == 1) and not self.is_auth:
            self.view.Control_tabWidget.setCurrentIndex(0)
            dialog = QtWidgets.QInputDialog(self.view)
            password, ok = dialog.getText(self.view, " ", "Пароль:")

            if ok and password == self.password:
                self.is_auth = True
                self.view.Control_tabWidget.setCurrentIndex(index)
            else:
                QtWidgets.QMessageBox.warning(self.view, 'ОШИБКА', "В доступе отказано")
                self.view.Control_tabWidget.setCurrentIndex(0)

    def check_password_listWidget(self, index):
        if (index != 4) and not self.is_auth:
            self.view.listWidget.setCurrentRow(4)
            self.view.stackedWidget.setCurrentIndex(5)
            dialog = QtWidgets.QInputDialog(self.view)
            password, ok = dialog.getText(self.view, " ", "Пароль:")

            if ok and password == self.password:
                self.is_auth = True
                self.view.listWidget.setCurrentRow(index)
                self.view.stackedWidget.setCurrentIndex(index + 1)
            else:
                QtWidgets.QMessageBox.warning(self.view, 'ОШИБКА', "В доступе отказано")
                self.view.stackedWidget.setCurrentIndex(5)

    def check_password_tabWidget(self, index):
        if (index == 1) and not self.is_auth:
            self.view.tabWidget.setCurrentIndex(0)
            dialog = QtWidgets.QInputDialog(self.view)
            password, ok = dialog.getText(self.view, " ", "Пароль:")

            if ok and password == self.password:
                self.is_auth = True
                self.view.tabWidget.setCurrentIndex(index)
            else:
                QtWidgets.QMessageBox.warning(self.view, 'ОШИБКА', "В доступе отказано")
                self.view.tabWidget.setCurrentIndex(0)
