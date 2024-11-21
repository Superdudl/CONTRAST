import platform
from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore
import numpy as np
from matplotlib.pyplot import imshow
from pathlib import PurePath, Path


class ParamsController(QObject):
    def __init__(self, view, video_cap, measure_controller, led_controller):
        super().__init__()
        self.view = view
        self.led_controller = led_controller
        self.video_cap = video_cap
        self.measure_controller = measure_controller
        self.setupUI()

        # Назначение выдержки
        if platform.system() != 'Windows':
            self.time_exposition = self.video_cap.camera.capture_metadata()['ExposureTime']
            self.time_exposition = np.around(self.time_exposition / 1000)*1000
        else:
            self.time_exposition = 5e4
        self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))

        # Назначение ШИМ
        self.white_pwm = int(self.video_cap.ctrls["White_PWM"])
        self.ir_pwm = int(self.video_cap.ctrls["White_PWM"])
        self.view.White_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))
        self.view.IR_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))


    def setupUI(self):
        # Настройка захвата изображения
        self.view.EN_Hist_checkBox.clicked.connect(self.hist_checkbox)
        self.view.Capture_image_checkBox.clicked.connect(self.capture_checkbox)

        # Настройка выдержки
        self.view.Exposition_minus_pushButton.clicked.connect(self.minus_exposition)
        self.view.Exposition_plus_pushButton.clicked.connect(self.plus_exposition)
        self.view.Exposition_Apply_pushButton.clicked.connect(self.apply_exposition)

        # Настройка списка настроек
        self.view.listWidget.itemClicked.connect(self.show_params_window_user)
        self.view.listWidget_2.itemClicked.connect(self.show_params_window_service)

        # Настройка ШИМ
        self.view.White_LED_minus_pushButton.clicked.connect(self.minus_white_led)
        self.view.White_LED_plus_pushButton.clicked.connect(self.plus_white_led)
        self.view.IR_LED_minus_pushButton.clicked.connect(self.minus_ir_led)
        self.view.IR_LED_plus_pushButton.clicked.connect(self.plus_ir_led)
        self.view.White_LED_Switch.clicked.connect(self.switch_white)
        self.view.IR_LED_Switch.clicked.connect(self.switch_ir)

        # Восстановить заводские настройки
        calib_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'calib_config.npy')
        factory_calib_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'calib_config.npy')
        if Path(factory_calib_file).exists():
            self.video_cap.calib_LUT = np.load(Path(factory_calib_file))
            Path(calib_file).unlink(missing_ok=True)

    def switch_white(self, button):
        if self.view.White_LED_Switch.isChecked():
            self.led_controller.set_white_led_pwm(duty=self.white_pwm)
        else:
            self.led_controller.set_white_led_pwm(duty=0)

    def switch_ir(self, button):
        if self.view.IR_LED_Switch.isChecked():
            self.led_controller.set_ir_led_pwm(duty=self.ir_pwm)
        else:
            self.led_controller.set_ir_led_pwm(duty=0)

    def minus_white_led(self):
        self.white_pwm -= 10
        if self.white_pwm < 0:
            self.white_pwm = 0
        if platform.system() != 'Windows':
            self.led_controller.set_white_led_pwm(duty=self.white_pwm)
        self.view.White_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))

    def plus_white_led(self):
        self.white_pwm += 10
        if self.white_pwm > 100:
            self.white_pwm = 100
        if platform.system() != 'Windows':
            self.led_controller.set_white_led_pwm(duty=self.white_pwm)
        self.view.White_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))

    def minus_ir_led(self):
        self.ir_pwm -= 10
        if self.ir_pwm < 0:
            self.ir_pwm = 0
        if platform.system() != 'Windows':
            self.led_controller.set_ir_led_pwm(duty=self.ir_pwm)
        self.view.IR_LED_lineEdit.setText(str(self.ir_pwm).replace('.', ','))

    def plus_ir_led(self):
        self.ir_pwm += 10
        if self.ir_pwm > 100:
            self.ir_pwm = 100
        if platform.system() != 'Windows':
            self.led_controller.set_ir_led_pwm(duty=self.ir_pwm)
        self.view.IR_LED_lineEdit.setText(str(self.ir_pwm).replace('.', ','))


    def show_params_window_user(self, item):
        index = self.view.listWidget.row(item)
        self.view.stackedWidget.setCurrentIndex(index + 1)

    def show_params_window_service(self, item):
        index = self.view.listWidget_2.row(item)
        self.view.stackedWidget_2.setCurrentIndex(index + 1)

    def hist_checkbox(self):
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

    def capture_checkbox(self):
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
            self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))

    def minus_exposition(self):
        if self.time_exposition - 5e2 >= 0:
            self.time_exposition -= 5e2
            self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))

    def apply_exposition(self):
        if platform.system() != 'Windows':
            self.video_cap.camera.set_controls({'ExposureTime': int(self.time_exposition)})
            print(self.video_cap.camera.capture_metadata()['ExposureTime'])
