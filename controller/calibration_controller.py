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
        self.gray_temp = Mera()
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
            self.video_cap.gray_templates = self.gray_temp.nominal_value
            calib_path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gray_templates.npy')
            np.save(Path(calib_path), np.array(self.gray_temp.nominal_value))

            nominals_path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'nominals.txt')
            np.savetxt(Path(nominals_path),
                       [self.mera.nominal_value[0], self.mera.nominal_value[1], self.mera.nominal_value[2]])

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
            ADC = np.uint8(np.mean(self.video_cap.frame_bw_orig[y1:y2, x1:x2]))
            self.mera.ADC[self.mera.id - 1] = ADC
            self.view.Measure_mera_lineEdit.setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
            for row in range(self.view.Mera_Table.rowCount()):
                if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                    self.view.Mera_Table.item(row, 1).setText(str(self.mera.ADC[self.mera.id - 1]).replace('.', ','))
                    break

    def add_mera(self):
        nominals_path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'nominals.txt')
        nominals = np.loadtxt(Path(nominals_path), dtype=float)
        x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
        x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
        ADC = np.uint8(np.mean(self.video_cap.frame_bw_noLUT[y1:y2, x1:x2]))
        if self.mera.id is None:
            self.mera.add_mera(ADC, nominals[0])
        elif len(self.mera) == 1:
            self.mera.add_mera(ADC, nominals[1])
        elif len(self.mera) == 2:
            self.mera.add_mera(ADC, nominals[2])
        else:
            self.mera.add_mera(ADC, 1.0)
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
            if np.mean(self.video_cap.orig_frame) < 100:
                self.video_cap.dark = self.video_cap.orig_frame
                dark_path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'dark_config.npy')
                np.save(dark_path, self.video_cap.dark)
                self.video_cap.gain = None
            else:
                self.video_cap.gain = calc_gain(self.video_cap.frame)
                gain_path = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gain_config.npy')
                np.save(gain_path, self.video_cap.gain)
        else:
            if self.view.units.isChecked():
                nominal = 10 ** -np.array(self.mera.nominal_value)
            elif self.view.units3.isChecked():
                nominal = 1 / np.array(self.mera.nominal_value)
            elif self.view.units2.isChecked():
                nominal = np.array(self.mera.nominal_value)
            k, b = calibrate(self.mera.ADC, nominal)
            self.calib_nominal = k * np.linspace(0, 255, 256) + b
            self.calib_nominal = np.clip(self.calib_nominal, 0, 1)

            # Присваиваем значения на прямой серым образцам
            x1_1 = int(self.video_cap.calib_obj_crosshair[0][0] - self.video_cap.calib_obj_crosshair[2] / 1.42)
            x1_2 = int(self.video_cap.calib_obj_crosshair[0][0] + self.video_cap.calib_obj_crosshair[2] / 1.42)
            x2_1 = int(self.video_cap.calib_obj_crosshair[1][0] - self.video_cap.calib_obj_crosshair[2] / 1.42)
            x2_2 = int(self.video_cap.calib_obj_crosshair[1][0] + self.video_cap.calib_obj_crosshair[2] / 1.42)
            y1_1 = int(self.video_cap.calib_obj_crosshair[0][1] - self.video_cap.calib_obj_crosshair[2] / 1.42)
            y1_2 = int(self.video_cap.calib_obj_crosshair[0][1] + self.video_cap.calib_obj_crosshair[2] / 1.42)
            y2_1 = int(self.video_cap.calib_obj_crosshair[1][1] - self.video_cap.calib_obj_crosshair[2] / 1.42)
            y2_2 = int(self.video_cap.calib_obj_crosshair[1][1] + self.video_cap.calib_obj_crosshair[2] / 1.42)
            ADC_obj_1 = (np.mean(self.video_cap.frame_bw_orig[y1_1:y1_2, x1_1:x1_2]) * 1.5).astype(np.uint8)
            ADC_obj_2 = (np.mean(self.video_cap.frame_bw_orig[y2_1:y2_2, x2_1:x2_2]) * 1.5).astype(np.uint8)
            gray_template_1 = self.calib_nominal[ADC_obj_1]
            gray_template_2 = self.calib_nominal[ADC_obj_2]
            if len(self.gray_temp) > 0:
                self.gray_temp.clear()
            self.gray_temp.add_mera(ADC_obj_1, gray_template_1)
            self.gray_temp.add_mera(ADC_obj_2, gray_template_2)

            for row in range(self.view.Mera_Table.rowCount()):
                ADC = np.uint8(float(self.view.Mera_Table.item(row, 1).text()))
                if self.view.units.isChecked():
                    res = np.log10(1 / np.array(self.calib_nominal[ADC]))
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
                    for row in range(self.view.Mera_Table.rowCount()):
                        if float(self.view.Mera_Table.item(row, 0).text()) > self.mera.id:
                            self.view.Mera_Table.item(row, 0).setText(
                                str(int(float(self.view.Mera_Table.item(row, 0).text())) - 1))
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
                self.mera.nominal_value[self.mera.id - 1] -= 0.01
                self.view.Nominal_lineEdit.setText(str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                for row in range(self.view.Mera_Table.rowCount()):
                    if self.view.Mera_Table.item(row, 0).text() == str(self.mera.id):
                        self.view.Mera_Table.item(row, 2).setText(
                            str(self.mera.nominal_value[self.mera.id - 1]).replace('.', ','))
                        break

    def plus_nominal(self):
        if self.mera.id is not None:
            if self.mera.nominal_value[self.mera.id - 1] < 100:
                self.mera.nominal_value[self.mera.id - 1] += 0.01
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
            if self.view.units.isChecked():
                nominal = 10 ** -np.array(self.mera.nominal_value)
            elif self.view.units3.isChecked():
                nominal = 1 / np.array(self.mera.nominal_value)
            elif self.view.units2.isChecked():
                nominal = np.array(self.mera.nominal_value)
            self.view.canvas.axes.cla()
            self.view.canvas.axes.scatter(self.mera.ADC, nominal, color='m', s=30)
            self.view.canvas.axes.scatter(self.gray_temp.ADC, self.gray_temp.nominal_value, color='b', s=30)
            if self.video_cap.calib_LUT is not None:
                self.view.canvas.axes.plot(self.video_cap.calib_LUT / 255, color='r')
            if self.calib_nominal is not None:
                self.view.canvas.axes.plot(np.linspace(0, 255, 256), self.calib_nominal)
            self.view.canvas.axes.set_xlim(0, 255)
            self.view.canvas.axes.set_ylim(0, 1)
            self.view.canvas.draw()
