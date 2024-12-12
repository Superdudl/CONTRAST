import platform
from PyQt5.QtCore import QObject, QSettings
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
        path = Path(PurePath(Path(__file__).parent.parent, 'src', 'settings.ini'))
        self.settings = QSettings(str(path), QSettings.Format.IniFormat)

        # Назначение выдержки
        if platform.system() != 'Windows':
            self.time_exposition = self.video_cap.camera.capture_metadata()['ExposureTime']
            self.time_exposition = np.around(self.time_exposition / 1000) * 1000
        else:
            self.time_exposition = 5e4
        self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))

        # Назначение ШИМ
        self.white_pwm = 50
        self.ir_pwm = 50
        self.view.White_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))
        self.view.IR_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))

    def setupUI(self):
        # Настройка захвата изображения
        self.view.EN_Hist_checkBox.clicked.connect(self.hist_checkbox)
        self.view.Capture_image_checkBox.clicked.connect(self.capture_checkbox)
        self.view.Hist_scale_checkbox.clicked.connect(self.hist_scale_checkbox)

        # Настройка выдержки
        self.view.Exposition_minus_pushButton.clicked.connect(self.minus_exposition)
        self.view.Exposition_plus_pushButton.clicked.connect(self.plus_exposition)

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
        self.view.recovery_settings_pushButton_2.clicked.connect(self.recover_calib)

        # Выбор единиц измерения
        self.view.units.clicked.connect(self.units_clicked)
        self.view.units2.clicked.connect(self.units_clicked)
        self.view.units3.clicked.connect(self.units_clicked)

    def recover_calib(self):
        gray_templates_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gray_templates.npy')
        factory_gray_templates_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_gray_templates.npy')
        gain_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gain_config.npy')
        factory_gain_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_gain_config.npy')
        dark_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'dark_config.npy')
        factory_dark_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_dark_config.npy')

        Path(gray_templates_file).unlink(missing_ok=True)
        Path(gain_file).unlink(missing_ok=True)
        Path(dark_file).unlink(missing_ok=True)

        if Path(factory_gray_templates_file).exists():
            self.video_cap.gray_templates = np.load(Path(factory_gray_templates_file))
        else:
            self.video_cap.gray_templates = None
            self.video_cap.calib_LUT = None
        if Path(factory_gain_file).exists():
            self.video_cap.gain = np.load(Path(factory_gain_file))
        else:
            self.video_cap.gain = None
        if Path(factory_dark_file).exists():
            self.video_cap.dark = np.load(Path(factory_dark_file))
        else:
            self.video_cap.dark = None

    def units_clicked(self):
        self.settings.setValue('units/units', self.view.units.isChecked())
        self.settings.setValue('units/units2', self.view.units2.isChecked())
        self.settings.setValue('units/units3', self.view.units3.isChecked())

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
        self.settings.setValue('whitePWM', self.white_pwm)

    def plus_white_led(self):
        self.white_pwm += 10
        if self.white_pwm > 100:
            self.white_pwm = 100
        if platform.system() != 'Windows':
            self.led_controller.set_white_led_pwm(duty=self.white_pwm)
        self.view.White_LED_lineEdit.setText(str(self.white_pwm).replace('.', ','))
        self.settings.setValue('whitePWM', self.white_pwm)

    def minus_ir_led(self):
        self.ir_pwm -= 10
        if self.ir_pwm < 0:
            self.ir_pwm = 0
        if platform.system() != 'Windows':
            self.led_controller.set_ir_led_pwm(duty=self.ir_pwm)
        self.view.IR_LED_lineEdit.setText(str(self.ir_pwm).replace('.', ','))
        self.settings.setValue('irPWM', self.ir_pwm)

    def plus_ir_led(self):
        self.ir_pwm += 10
        if self.ir_pwm > 100:
            self.ir_pwm = 100
        if platform.system() != 'Windows':
            self.led_controller.set_ir_led_pwm(duty=self.ir_pwm)
        self.view.IR_LED_lineEdit.setText(str(self.ir_pwm).replace('.', ','))
        self.settings.setValue('irPWM', self.ir_pwm)

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
        self.settings.setValue('img_capture_params/EN_Hist_checkBox', self.view.EN_Hist_checkBox.isChecked())

    def hist_scale_checkbox(self):
        self.settings.setValue('img_capture_params/Hist_scale_checkbox', self.view.Hist_scale_checkbox.isChecked())

    def capture_checkbox(self):
        if self.view.Capture_image_checkBox.isChecked():
            self.view.Measure_pushButton.setEnabled(False)
            self.settings.setValue('img_capture_params/Capture_image_checkBox',
                                   self.view.Capture_image_checkBox.isChecked())
        else:
            self.view.Measure_pushButton.setEnabled(True)
            self.settings.setValue('img_capture_params/Capture_image_checkBox',
                                   self.view.Capture_image_checkBox.isChecked())

    def plus_exposition(self):
        if self.time_exposition + 5e2 <= 1e5:
            self.time_exposition += 5e2
            self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))
        if platform.system() != 'Windows':
            self.video_cap.camera.set_controls({'ExposureTime': int(self.time_exposition)})
        self.settings.setValue('timeExposure', self.time_exposition)

    def minus_exposition(self):
        if self.time_exposition - 5e2 >= 0:
            self.time_exposition -= 5e2
            self.view.Exposition_lineEdit.setText(str(self.time_exposition / 1000).replace('.', ','))
        if platform.system() != 'Windows':
            self.video_cap.camera.set_controls({'ExposureTime': int(self.time_exposition)})
        self.settings.setValue('timeExposure', self.time_exposition)
