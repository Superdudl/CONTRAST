import platform
from pathlib import PurePath, Path

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem
from utils.calibration import Mera
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
        self.view.Calibrate_save_pushButton.clicked.connect(self.save_calibration)

    def save_calibration(self):
        if self.calib_nominal is not None:
            self.video_cap.calib_LUT = np.uint8(self.calib_nominal * 255)
            path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'calib_config')
            np.save(path, self.video_cap.calib_LUT)

    def change_nominal(self, text):
        if self.mera.id is not None and len(text) > 0:
            text = text.replace(',', '.')
            self.mera.nominal_value[self.mera.id - 1] = float(text)
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.item(row, 2).setText(
                        str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                    break

    def update_ADC(self):
        if self.mera.id is not None:
            x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
            x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
            ADC = np.uint8(np.mean(self.video_cap.frame_bw[y1:y2, x1:x2]))
            self.mera.ADC[self.mera.id - 1] = ADC
            self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.item(row, 1).setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
                    break

    def add_mera(self):
        x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
        x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
        ADC = np.uint8(np.mean(self.video_cap.frame_bw_orig[y1:y2, x1:x2]))

        self.mera.add_mera(ADC, np.random.randint(0, 100))
        self.view.Mera_number_lineEdit.setText(str(self.mera.id).replace('.', ','))
        self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
        self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
        self.view.Mera_num_max_label.setText(str(len(self.mera)).replace('.', ','))

        row_index = self.view.Mera_Table.rowCount()
        self.view.Mera_Table.insertRow(row_index)
        self.view.Mera_Table.setItem(row_index, 0, QTableWidgetItem(str(self.mera.id).replace('.', ',')))
        self.view.Mera_Table.setItem(row_index, 1,
                                     QTableWidgetItem(str(int(self.mera.ADC[self.mera.id - 1])).replace('.', ',')))
        self.view.Mera_Table.setItem(row_index, 2,
                                     QTableWidgetItem(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ',')))
        self.view.Mera_Table.setItem(row_index, 3, QTableWidgetItem(str('')))

    def calibrate(self):
        if self.mera.id is None and platform.system() != 'Windows':
            self.video_cap.gain = calc_gain(self.video_cap.frame_bw_orig)
        else:
            if self.view.units.isChecked():
                nominal = 10 ** -np.array(self.mera.nominal_value)
            elif self.view.units3.isChecked():
                nominal = 1 / np.array(self.mera.nominal_value)
            elif self.view.units2.isChecked():
                nominal = np.array(self.mera.nominal_value)
            k, b = calibrate(self.mera.ADC, nominal)
            self.calib_nominal = k * np.linspace(0, 255, 256) + b

            for row in range(self.view.Mera_Table.rowCount()):
                ADC = np.uint8(float(self.view.Mera_Table.item(row, 1).text()))
                if self.view.units.isChecked():
                    res = 10 ** -np.array(self.calib_nominal[ADC])
                    self.view.Mera_Table.item(row, 3).setText(f'{res:.2f}'.replace('.', ','))
                elif self.view.units3.isChecked():
                    res = 1 / np.array(self.calib_nominal[ADC])
                    self.view.Mera_Table.item(row, 3).setText(f'{res:.2f}'.replace('.', ','))
                elif self.view.units2.isChecked():
                    res = np.array(self.calib_nominal[ADC])
                    self.view.Mera_Table.item(row, 3).setText(f'{res:.2f}'.replace('.', ','))

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
            self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
            self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
            self.view.Mera_number_lineEdit.setText(str(self.mera.id).replace('.', ','))
        self.view.Mera_num_max_label.setText(str(len(self.mera)).replace('.', ','))

    def minus_nominal(self):
        if self.mera.id is not None:
            if self.mera.nominal_value[self.mera.id - 1] > 0:
                self.mera.nominal_value[self.mera.id - 1] -= 1
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                for row in range(self.view.Mera_Table.rowCount()):
                    if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                        self.view.Mera_Table.item(row, 2).setText(
                            str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                        break

    def plus_nominal(self):
        if self.mera.id is not None:
            if self.mera.nominal_value[self.mera.id - 1] < 100:
                self.mera.nominal_value[self.mera.id - 1] += 1
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                for row in range(self.view.Mera_Table.rowCount()):
                    if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                        self.view.Mera_Table.item(row, 2).setText(
                            str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                        break

    def minus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id - 1 >= 1:
                self.mera.id -= 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id).replace('.', ','))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))

    def plus_mera_num(self):
        if len(self.mera) > 0:
            if self.mera.id + 1 <= len(self.mera):
                self.mera.id += 1
                self.view.Mera_number_lineEdit.setText(str(self.mera.id).replace('.', ','))
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))

    def update_plot(self, index):
        if index == 1:
            index = np.argsort(self.mera.ADC)
            sorted_ADC = np.array(self.mera.ADC)[index]
            if self.view.units.isChecked():
                sorted_nominal = 10 ** -np.array(self.mera.nominal_value)[index]
            elif self.view.units3.isChecked():
                sorted_nominal = 1 / np.array(self.mera.nominal_value)[index]
            elif self.view.units2.isChecked():
                sorted_nominal = np.array(self.mera.nominal_value)[index]
            self.view.canvas.axes.cla()
            self.view.canvas.axes.scatter(sorted_ADC, sorted_nominal, color='m', s=30)
            if self.calib_nominal is not None:
                self.view.canvas.axes.plot(np.linspace(0, 255, 256), self.calib_nominal)
            self.view.canvas.axes.set_xlim(0, 255)
            self.view.canvas.draw()
