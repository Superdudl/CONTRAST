from view import CameraApp
from PyQt5 import QtCore
import numpy as np


class Calibration(CameraApp):
    def __init__(self):
        super().__init__()
        self.Nominal_minus_pushButton.clicked.connect(self.minus_nominal)
        self.Nominal_plus_pushButton.clicked.connect(self.plus_nominal)
        self.Mera_push_pushButton.clicked.connect(self.add_mera)
        self.Mera_delete_pushButton.clicked.connect(self.delete_mera)
        self.Mera_number_minus_pushButton.clicked.connect(self.minus_mera_num)
        self.Mera_number_plus_pushButton.clicked.connect(self.plus_mera_num)

    def add_mera(self):
        self.mera.add_mera(np.random.randint(0, 255), np.random.randint(0, 100))
        if self.mera_id is None:
            self.mera_id = 1
            self.Mera_number_lineEdit.setText(str(self.mera_id))
            self.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera_id - 1]))
        else:
            self.mera_id += 1
            self.Mera_number_lineEdit.setText(str(self.mera_id))
            self.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera_id - 1]))
        _translate = QtCore.QCoreApplication.translate
        self.Mera_num_max_label.setText(_translate("Widget", str(len(self.mera))))

    def delete_mera(self):
        if self.mera_id is None:
            pass
        else:
            self.mera.delete_mera(self.mera_id - 1)
            if len(self.mera) == 0:
                self.mera_id = None
                self.Nominal_lineEdit.setText('')
                self.Mera_number_lineEdit.setText('')
            elif self.mera_id > len(self.mera):
                self.mera_id = len(self.mera)
                self.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera_id - 1]))
                self.Mera_number_lineEdit.setText(str(self.mera_id))
            else:
                if self.mera_id != 1:
                    self.mera_id -= 1
                self.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera_id - 1]))
                self.Mera_number_lineEdit.setText(str(self.mera_id))
        _translate = QtCore.QCoreApplication.translate
        self.Mera_num_max_label.setText(_translate("Widget", str(len(self.mera))))
