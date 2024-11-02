import platform
from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore


class ParamsController(QObject):
    def __init__(self, view, video_cap, measure_conroller):
        super().__init__()
        self.view = view
        self.video_cap = video_cap
        self.measure_controller = measure_conroller
        self.setupUI()
        if platform.system() != 'Windows':
            self.time_exposition = self.video_cap.camera.capture_metadata()['ExposureTime'] + 1
        else:
            self.time_exposition = 5e4
        self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000))

    def setupUI(self):
        # Настройка захвата изображения
        self.view.Apply_capture_image_pushButton.clicked.connect(self.apply_img_capture_params)

        # Настройка выдержки
        self.view.Exposition_minus_pushButton.clicked.connect(self.minus_exposition)
        self.view.Exposition_plus_pushButton.clicked.connect(self.plus_exposition)
        self.view.Exposition_Apply_pushButton.clicked.connect(self.apply_exposition)

        # Настройка списка настроек
        self.view.listWidget.itemClicked.connect(self.show_params_window_user)
        self.view.listWidget_2.itemClicked.connect(self.show_params_window_service)

    def show_params_window_user(self, item):
        index = self.view.listWidget.row(item)
        self.view.stackedWidget.setCurrentIndex(index + 1)

    def show_params_window_service(self, item):
        index = self.view.listWidget_2.row(item)
        self.view.stackedWidget_2.setCurrentIndex(index + 1)

    def apply_img_capture_params(self):
        if self.view.EN_Hist_checkBox.isChecked():
            self.view.Hist_Widget.show()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 220, 300, 140))
            font = QtGui.QFont()
            font.setPointSize(30)
            self.view.Contrast_Label.setFont(font)
        else:
            self.view.Hist_Widget.hide()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 130, 300, 140))
            font = QtGui.QFont()
            font.setPointSize(100)
            self.view.Contrast_Label.setFont(font)

        if self.view.Capture_image_checkBox.isChecked():
            self.view.Measure_pushButton.setEnabled(False)
            self.video_cap.timer.timeout.connect(self.measure_controller.motion_detector)
        else:
            self.view.Measure_pushButton.setEnabled(True)
            try:
                self.video_cap.timer.timeout.disconnect(self.measure_controller.motion_detector)
            except TypeError:
                pass


    def plus_exposition(self):
        if self.time_exposition + 5e2 <= 1e5:
            self.time_exposition += 5e2
        self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000))

    def minus_exposition(self):
        if self.time_exposition - 5e2 >= 0:
            self.time_exposition -= 5e2
        self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000))

    def apply_exposition(self):
        if platform.system() != 'Windows':
            self.video_cap.camera.set_controls({'ExposureTime': int(self.time_exposition)})
