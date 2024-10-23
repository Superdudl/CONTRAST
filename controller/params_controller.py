import platform
from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore
from fontTools.ttLib.tables.E_B_L_C_ import eblc_index_sub_table_4, eblc_index_sub_table_3

from tst_picam_12_10_1 import time_exposition


class ParamsController(QObject):
    def __init__(self, view, video_cap):
        super().__init__()
        self.view = view
        self.video_cap = video_cap
        self.setupUI()

    def setupUI(self):
        # Параметры захвата изображения
        self.view.Apply_capture_image_pushButton.clicked.connect(self.apply_img_capture_params)

        # Выдержка
        self.view.Exposition_minus_pushButton.clicked.connect(self.minus_exposition)
        self.view.Exposition_plus_pushButton.clicked.connect(self.plus_exposition)
        self.view.Exposition_Apply_pushButton.clicked.connect(self.apply_exposition)

        # Окно изменения настройки
        self.view.listWidget.currentRowChanged['int'].connect(self.show_params_window_user)
        self.view.listWidget_2.currentRowChanged['int'].connect(self.show_params_window_service)

    def show_params_window_user(self, index):
        self.view.stackedWidget.setCurrentIndex(index)
        self.view.stackedWidget.show()

    def show_params_window_service(self, index):
        self.view.stackedWidget_2.setCurrentIndex(index)
        self.view.stackedWidget_2.show()

    def apply_img_capture_params(self):
        if self.view.EN_Hist_checkBox.isChecked():
            self.view.Hist_Label.show()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(50, 240, 300, 120))
            font = QtGui.QFont()
            font.setPointSize(30)
            self.view.Contrast_Label.setFont(font)
        else:
            self.view.Hist_Label.hide()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(50, 130, 300, 120))
            font = QtGui.QFont()
            font.setPointSize(100)
            self.view.Contrast_Label.setFont(font)

    def plus_exposition(self):
        if platform.system() == 'Windows':
            self.time_exposition = 5e4
        else:
            self.time_exposition = int(self.video_cap.camera.capture_metadata()['ExposureTime'])
        if self.time_exposition + 5e3 <= 1e5:
            self.time_exposition += 5e3
        self.view.Exposition_lineEdit.setText(str(int(self.time_exposition // 1000)))

    def minus_exposition(self):
        if platform.system() == 'Windows':
            self.time_exposition = 5e4
        else:
            self.time_exposition = int(self.video_cap.camera.capture_metadata()['ExposureTime'])
        if self.time_exposition - 5e3 >= 0:
            self.time_exposition -= 5e3
        self.view.Exposition_lineEdit.setText(str(int(self.time_exposition // 1000)))

    def apply_exposition(self):
        if platform.system() != 'Windows':
            self.camera.set_controls({'ExposureTime': self.time_exposition})