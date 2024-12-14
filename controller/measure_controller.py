from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from numpy import empty
from utils import histogram, calc_contrast
import numpy as np
import cv2
import platform


class ContrastThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, video_cap, view, led, avg_num=3):
        super().__init__()
        self.video_cap = video_cap
        self.view = view
        self.led = led
        self.avg_num = np.clip(avg_num, 1, None)

    def run(self):
        pwm = self.led.white_pwm
        self.view.Measure_pushButton.setEnabled(False)
        self.led.set_white_led_pwm(0)

        x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
        x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
        frame = self.video_cap.frame_bw[y1:y2, x1:x2]
        result = []
        for i in range(0, self.avg_num):
            res = calc_contrast(frame)
            result.append(res['contrast'])
            self.video_cap.update_frame(update_preview=False)
            frame = self.video_cap.frame_bw[y1:y2, x1:x2]
                
        res = np.mean(result)

        if platform.system != 'Windows':
            cv2.imwrite('/home/contrast/shared/YUV.png', self.video_cap.frame)
        self.led.set_white_led_pwm(pwm)
        if res is not None and self.view.units.isChecked():
            res = np.log10(res)
        elif res is None:
            self.view.Contrast_Label.setText('-')
        if self.view.user_mode.isChecked():
            MIN = float(self.view.label_MIN_input.text().replace(',', '.'))
            MAX = float(self.view.label_MAX_input.text().replace(',', '.'))

            if res is not None and MIN < res < MAX:
                res = 'НОРМ'
            elif res is not None and res < MIN:
                res = 'МИН'
            elif res is not None and res > MAX:
                res = 'МАКС'
            self.view.Contrast_Label.setText(res)
        if self.view.expert_mode.isChecked():
            self.view.Contrast_Label.setText(f'{res:.2f}'.replace('.', ','))
        self.finished_signal.emit()


class MeasureController(QObject):
    def __init__(self, view, video_cap, led):
        super().__init__()
        self.video_cap = video_cap
        self.view = view
        self.led = led
        self.worker = None
        self.setupUI()

    def setupUI(self):
        # Гистограмма
        self.timer = QTimer()
        self.video_cap.timer.timeout.connect(self.calc_hist)
        self.video_cap.timer.timeout.connect(self.motion_detector)
        self.timer.start(100)

        # Измерение
        self.view.Measure_pushButton.clicked.connect(self.calc_contrast)

    def calc_hist(self):
        x1, y1 = self.video_cap.crosshair[0][0], self.video_cap.crosshair[0][1]
        x2, y2 = self.video_cap.crosshair[1][0], self.video_cap.crosshair[1][1]
        self.frame = self.video_cap.frame_bw[y1:y2, x1:x2]
        self.hist = histogram(self.frame, log=self.view.Hist_scale_checkbox.isChecked())
        self.qimage = QImage(self.hist, 384, 192, 384 * 3, QImage.Format_RGB888)
        self.view.Hist_Label.setPixmap(QPixmap.fromImage(self.qimage))

    def calc_contrast(self):
        def start_timer():
            self.video_cap.update_frame(update_preview=True)
            self.video_cap.timer.start()
            if not self.view.Capture_image_checkBox.isChecked():
                self.view.Measure_pushButton.setEnabled(True)

        if self.worker is not None:
            if self.worker.isRunning():
                return
        self.video_cap.timer.stop()
        self.worker = ContrastThread(self.video_cap, self.view, self.led)
        self.worker.finished_signal.connect(start_timer)
        self.worker.start()
        frame_prewiew = self.video_cap.frame_preview
        rect = np.zeros_like(frame_prewiew)
        rect = cv2.rectangle(rect, [0, 0], [rect.shape[1], rect.shape[0]], color=(255, 0, 0), thickness=20)
        qimage = QImage(cv2.addWeighted(frame_prewiew, 0.5, rect, 0.5, gamma=1.0), 360, 480, 360 * 3,
                        QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(qimage))

    def motion_detector(self):
        if self.view.Capture_image_checkBox.isChecked() and self.view.tabWidget.currentIndex() == 0:
            if self.video_cap.prev_frame is not None or self.video_cap.prev_frame is not empty:
                curr = cv2.cvtColor(self.video_cap.frame_preview, cv2.COLOR_RGB2GRAY)
                curr = cv2.GaussianBlur(curr, (21, 21), 3)

                try:
                    prev = cv2.cvtColor(self.video_cap.prev_frame, cv2.COLOR_RGB2GRAY)
                    prev = cv2.GaussianBlur(prev, (21, 21), 3)
                except cv2.error as e:
                    prev = np.zeros_like(curr)

                diff = cv2.absdiff(prev, curr)
        
                if diff[diff < 2].size / diff.size > 0.98:
                    self.calc_contrast()

