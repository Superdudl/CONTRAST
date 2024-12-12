from sys import platform

from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSettings
from pathlib import Path, PurePath
from controller import CalibrationController, VideoCapture, ParamsController, MeasureController, LedController, \
    Authentication
import platform
import subprocess


class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.connect_controllers()
        self.connect_slots()
        path = Path(PurePath(Path(__file__).parent.parent, 'src', 'settings.ini'))
        self.settings = QSettings(str(path), QSettings.Format.IniFormat)
        self.setupUI()

    def setupUI(self):
        # Восстановление сеанса гистограммы
        if self.settings.value('img_capture_params/EN_Hist_checkBox', type=bool):
            self.view.Hist_Widget.show()
            self.view.EN_Hist_checkBox.setChecked(self.settings.value('img_capture_params/EN_Hist_checkBox', type=bool))
            self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 220, 300, 140))
            font = QtGui.QFont()
            font.setPointSize(30)
            self.view.Contrast_Label.setFont(font)
            self.view.Hist_scale_checkbox.setChecked(
                self.settings.value('img_capture_params/Hist_scale_checkbox', type=bool))
        else:
            self.view.Hist_Widget.hide()
            self.view.EN_Hist_checkBox.setChecked(self.settings.value('img_capture_params/EN_Hist_checkBox', type=bool))
            self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 130, 300, 140))
            font = QtGui.QFont()
            font.setPointSize(100)
            self.view.Contrast_Label.setFont(font)
        self.view.Contrast_Label.setFont(font)
        self.view.Contrast_Label.setText("0,00")

        # Восстановление режима захвата при движении

        self.view.Capture_image_checkBox.setChecked(
            self.settings.value('img_capture_params/Capture_image_checkBox', False, type=bool))

        if self.view.Capture_image_checkBox.isChecked():
            self.view.Measure_pushButton.setEnabled(False)
        else:
            self.view.Measure_pushButton.setEnabled(True)

        # Восстановление выдержки и ШИМ
        if platform.system() != "Windows":
            self.led_controller.set_white_led_pwm(self.settings.value('whitePWM', type=int))
            self.led_controller.set_ir_led_pwm(self.settings.value('irPWM', type=int))
            self.video_capture.camera.set_controls({'ExposureTime': self.settings.value('timeExposure', type=int)})

        self.params_controller.time_exposition = self.settings.value('timeExposure',
                                                                     self.params_controller.time_exposition, type=int)
        self.view.Exposition_lineEdit.setText(
            str(self.settings.value('timeExposure', defaultValue=int(self.video_capture.ctrls["ExposureTime"]),
                                    type=int) / 1000).replace('.', ','))
        self.view.IR_LED_lineEdit.setText(
            str(self.settings.value('irPWM', defaultValue=self.params_controller.white_pwm, type=int)))
        self.view.White_LED_lineEdit.setText(
            str(self.settings.value('whitePWM', defaultValue=self.params_controller.ir_pwm, type=int)))
        self.params_controller.white_pwm = self.settings.value('whitePWM',
                                                               defaultValue=self.params_controller.white_pwm, type=int)
        self.params_controller.ir_pwm = self.settings.value('irPWM', defaultValue=self.params_controller.white_pwm,
                                                            type=int)

        # Востановление состояния кнопок измерения
        self.view.units.setChecked(self.settings.value('units/units', type=bool))
        self.view.units2.setChecked(self.settings.value('units/units2', type=bool))
        self.view.units3.setChecked(self.settings.value('units/units3', type=bool))

    def connect_controllers(self):
        self.video_capture = VideoCapture(self.view)
        self.led_controller = LedController()
        self.measure_controller = MeasureController(self.view, self.video_capture, self.led_controller)
        self.calibration_controller = CalibrationController(self.view, self.video_capture)
        self.params_controller = ParamsController(self.view, self.video_capture, self.measure_controller,
                                                  self.led_controller)
        self.authenticated_controller = Authentication(self.view)

    def connect_slots(self):
        self.view.power_button.clicked.connect(self.power_off)

    def power_off(self):
        if platform.system() != "Windows":
            try:
                subprocess.run(["sudo", "shutdown", "now"], check=True)
                print("Выключение...")
            except subprocess.CalledProcessError as e:
                print(f'Error: {e}')
