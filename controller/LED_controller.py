import platform
from PyQt5.QtCore import QObject
if platform.system() != 'Windows':
    import pigpio

class LedController(QObject):
    def __init__(self):
        super().__init__()
        if platform.system() != 'Windows':
            self.gpio = pigpio.pi()
            self.gpio.write(6,1)
            self.gpio.set_PWM_frequency(12, 8000)
            self.gpio.set_PWM_frequency(13, 8000)
            self.gpio.set_PWM_range(12, 100)
            self.gpio.set_PWM_range(13, 100)
            self.gpio.set_PWM_dutycycle(12, 0)
            self.gpio.set_PWM_dutycycle(13, 0)

    def set_white_led_pwm(self, duty):
        self.gpio.set_PWM_dutycycle(13, duty)

    def set_ir_led_pwm(self, duty):
        self.gpio.set_PWM_dutycycle(12, duty)