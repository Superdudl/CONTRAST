from sys import platform

from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSettings
from pathlib import Path, PurePath
from controller import CalibrationController, VideoCapture, ParamsController, MeasureController, LedController
import platform


class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.connect_controllers()
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
        else:
            self.view.Hist_Widget.hide()
            self.view.EN_Hist_checkBox.setChecked(self.settings.value('img_capture_params/EN_Hist_checkBox', type=bool))
            self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 130, 300, 140))
            font = QtGui.QFont()
            font.setPointSize(100)
            self.view.Contrast_Label.setFont(font)
        self.view.Contrast_Label.setFont(font)
        self.view.Contrast_Label.setText("0,00")

        if platform.system() != "Windows":
            self.led_controller.set_white_led_pwm(self.settings.value('whitePWM', type=int))
            self.led_controller.set_ir_led_pwm(self.settings.value('irPWM', type=int))
            self.video_capture.camera.set_controls({'ExposureTime': self.settings.value('timeExposure', type=int)})
        self.view.Exposition_lineEdit.setText(
            str(self.settings.value('timeExposure', defaultValue=int(self.video_capture.ctrls["ExposureTime"]), type=int) / 1000).replace('.', ','))
        self.view.IR_LED_lineEdit.setText(str(self.settings.value('whitePWM', defaultValue=self.video_capture.ctrls["IR_PWM"], type=int)))
        self.view.White_LED_lineEdit.setText(str(self.settings.value('irPWM',self.video_capture.ctrls["White_PWM"], type=int)))

        # Восстановление захвата по движению

        # Востановление состояния кнопок измерения
        self.view.units.setChecked(self.settings.value('units/units', type=bool))
        self.view.units2.setChecked(self.settings.value('units/units2', type=bool))
        self.view.units3.setChecked(self.settings.value('units/units3', type=bool))

    def connect_controllers(self):
        self.video_capture = VideoCapture(self.view)
        self.led_controller = LedController()
        self.measure_controller = MeasureController(self.view, self.video_capture)
        self.calibration_controller = CalibrationController(self.view, self.video_capture)
        self.params_controller = ParamsController(self.view, self.video_capture, self.measure_controller,
                                                  self.led_controller)
