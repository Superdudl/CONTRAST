from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtCore


class Authentication:
    def __init__(self, view):
        self.view = view
        self.is_auth = False
        self.connect_slots()

    def connect_slots(self):
        self.view.tabWidget.currentChanged.connect(self.check_password)

    def check_password(self, index):
        if (index == 1 or index == 2) and not self.is_auth:
            self.view.tabWidget.setCurrentIndex(0)
            dialog = QtWidgets.QInputDialog(self.view)
            password, ok = dialog.getText(self.view, " ", "Пароль:")

            if ok and password == '3113':
                self.is_auth = True
                self.view.tabWidget.setCurrentIndex(index)
            else:
                QtWidgets.QMessageBox.warning(self.view, 'ОШИБКА', "В доступе отказано")
                self.view.tabWidget.setCurrentIndex(0)


