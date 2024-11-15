import platform

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
from fontTools.merge.tables import merge

from utils.calibration import Mera
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
import numpy as np
from utils import calc_gain, calibrate


class CalibrationController(QObject):
    def __init__(self, view, video_cap):
        super().__init__()
        self.view = view
        self.video_cap = video_cap
        self.setupUI(self.view)
        self.mera = Mera()
        self.calib_nominal = None

    def setupUI(self, view):
        self.view.Nominal_minus_pushButton.clicked.connect(self.minus_nominal)
        self.view.Nominal_plus_pushButton.clicked.connect(self.plus_nominal)
        self.view.Mera_push_pushButton.clicked.connect(self.add_mera)
        self.view.Mera_delete_pushButton.clicked.connect(self.delete_mera)
        self.view.Mera_number_minus_pushButton.clicked.connect(self.minus_mera_num)
        self.view.Mera_number_plus_pushButton.clicked.connect(self.plus_mera_num)
        self.view.Refresh_ADC_pushButton.clicked.connect(self.update_ADC)
        self.view.Calibrate_start_pushButton.clicked.connect(self.calibrate)
        self.view.Calib_tab.currentChanged.connect(self.update_plot)
        self.view.Nominal_lineEdit.textChanged.connect(self.change_nominal)
        validator = QDoubleValidator(0.0, 100.0, 2)
        self.view.Nominal_lineEdit.setValidator(validator)

    def change_nominal(self, text):
        if self.mera.id is not None and len(text) > 0:
            text = text.replace(',', '.')
            self.mera.nominal_value[self.mera.id - 1] = float(text)
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.item(row, 2).setText(str(self.mera.nominal_value[self.mera.id - 1]))
                    break

    def update_ADC(self):
        if self.mera.id is not None:
            x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
            x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
            ADC = np.uint8(np.mean(self.video_cap.frame_bw[y1:y2, x1:x2]))
            self.mera.ADC[self.mera.id - 1] = ADC
            self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]))
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.item(row, 1).setText(str(self.mera.ADC[self.mera.id - 1]))
                    break

    def add_mera(self):
        x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
        x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
        ADC = np.uint8(np.mean(self.video_cap.frame_bw[y1:y2, x1:x2]))

        self.mera.add_mera(ADC, np.random.randint(0, 100))
        self.view.Mera_number_lineEdit.setText(str(self.mera.id))
        self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
        self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]))
        self.view.Mera_num_max_label.setText(str(len(self.mera)))

        row_index = self.view.Mera_Table.rowCount()
        self.view.Mera_Table.insertRow(row_index)
        self.view.Mera_Table.setItem(row_index, 0, QTableWidgetItem(str(self.mera.id)))
        self.view.Mera_Table.setItem(row_index, 1, QTableWidgetItem(str(int(self.mera.ADC[self.mera.id - 1]))))
        self.view.Mera_Table.setItem(row_index, 2, QTableWidgetItem(str(self.mera.nominal_value[self.mera.id - 1])))

    def calibrate(self):
        if self.mera.id is None and platform.system() != 'Windows':
            self.video_cap.gain = calc_gain(self.video_cap.frame_bw_orig)
        else:
            k, b = calibrate(self.mera.ADC, self.mera.nominal_value)
            self.calib_nominal = k * np.linspace(0, 255, 256) + b

    def delete_mera(self):
        if self.mera.id is not None:
            # Удаляем из таблицы
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.removeRow(row)
                    break

            self.mera.delete_mera(self.mera.id - 1)

        if self.mera.id is None:
            self.view.Nominal_lineEdit.setText('')
            self.view.Mera_number_lineEdit.setText('')
            self.view.Measure_mera_lineEdit.setText('')
        else:
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
            self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]))
            self.view.Mera_number_lineEdit.setText(str(self.mera.id))
        self.view.Mera_num_max_label.setText(str(len(self.mera)))

    def minus_nominal(self):
        if self.mera.id is not None:
            if self.mera.nominal_value[self.mera.id - 1] > 0:
                self.mera.nominal_value[self.mera.id - 1] -= 1
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                for row in range(self.view.Mera_Table.rowCount()):
                    if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                        self.view.Mera_Table.item(row, 2).setText(str(self.mera.nominal_value[self.mera.id - 1]))
                        break

    def plus_nominal(self):
        if self.mera.id is not None:
            if self.mera.nominal_value[self.mera.id - 1] < 100:
                self.mera.nominal_value[self.mera.id - 1] += 1
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                for row in range(self.view.Mera_Table.rowCount()):
                    if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                        self.view.Mera_Table.item(row, 2).setText(str(self.mera.nominal_value[self.mera.id - 1]))
                        break

    def minus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id - 1 >= 1:
                self.mera.id -= 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]))

    def plus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id + 1 <= len(self.mera):
                self.mera.id += 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]))
                self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]))

    def update_plot(self, index):
        if index == 1:
            index = np.argsort(self.mera.ADC)
            sorted_ADC = np.array(self.mera.ADC)[index]
            if self.view.calib_units.isChecked():
                sorted_nominal = np.pow(10, -np.array(self.mera.nominal_value)[index])
            else:
                sorted_nominal = 1 / np.array(self.mera.nominal_value)[index]
            self.view.canvas.axes.cla()
            self.view.canvas.axes.scatter(sorted_ADC, sorted_nominal, color='m', s=30)
            if self.calib_nominal is not None:
                self.view.canvas.axes.plot(np.linspace(0, 255, 256), self.calib_nominal)
            self.view.canvas.axes.set_xlim(0, 255)
            self.view.canvas.draw()
