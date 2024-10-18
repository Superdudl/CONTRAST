from utils.calibration import Mera
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
import numpy as np


class CalibrationController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setupUI(self.view)
        self.mera = Mera()

    def setupUI(self, view):
        self.view.Nominal_minus_pushButton.clicked.connect(self.minus_nominal)
        self.view.Nominal_plus_pushButton.clicked.connect(self.plus_nominal)
        self.view.Mera_push_pushButton.clicked.connect(self.add_mera)
        self.view.Mera_delete_pushButton.clicked.connect(self.delete_mera)
        self.view.Mera_number_minus_pushButton.clicked.connect(self.minus_mera_num)
        self.view.Mera_number_plus_pushButton.clicked.connect(self.plus_mera_num)

    def add_mera(self):
        self.mera.add_mera(np.random.randint(0, 255), 50)
        if self.mera.id is None:
            self.mera.id = 1
            self.view.Mera_number_lineEdit.setText(str(self.mera.id))
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
        else:
            self.mera.id += 1
            self.view.Mera_number_lineEdit.setText(str(self.mera.id))
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
        _translate = QtCore.QCoreApplication.translate
        self.view.Mera_num_max_label.setText(_translate("Widget", str(len(self.mera))))

    def delete_mera(self):
        if self.mera.id is None:
            pass
        else:
            self.mera.delete_mera(self.mera.id - 1)
            if len(self.mera) == 0:
                self.mera.id = None
                self.view.Nominal_lineEdit.setText('')
                self.view.Mera_number_lineEdit.setText('')
            elif self.mera.id > len(self.mera):
                self.mera.id = len(self.mera)
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
            else:
                if self.mera.id != 1:
                    self.mera.id -= 1
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
        _translate = QtCore.QCoreApplication.translate
        self.view.Mera_num_max_label.setText(_translate("Widget", str(len(self.mera))))

    def minus_nominal(self):
        if self.mera.nominal_value[self.mera.id - 1] > 0:
            self.mera.nominal_value[self.mera.id - 1] -= 1
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))

    def plus_nominal(self):
        if self.mera.nominal_value[self.mera.id - 1] < 100:
            self.mera.nominal_value[self.mera.id - 1] += 1
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))

    def minus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id - 1 >= 1:
                self.mera.id -= 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))

    def plus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id + 1 <= len(self.mera):
                self.mera.id += 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
