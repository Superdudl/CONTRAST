from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QImage, QPixmap
from utils import histogram, calc_contrast
import numpy as np
import cv2
import time


class MeasureController(QObject):
    def __init__(self, view, video_cap):
        super().__init__()
        self.video_cap = video_cap
        self.view = view
        self.setupUI()

    def setupUI(self):
        # Гистограмма
        self.timer = QTimer()
        self.timer.timeout.connect(self.calc_hist)
        self.timer.start(100)

        # Кнопка измерить
        self.view.Measure_pushButton.clicked.connect(self.calc_contrast)

    def calc_hist(self):
        self.frame = self.video_cap.frame_bw
        self.hist = histogram(self.frame)
        self.qimage = QImage(self.hist, 384, 192, 384 * 3, QImage.Format_RGB888)
        self.view.Hist_Label.setPixmap(QPixmap.fromImage(self.qimage))

    def calc_contrast(self):
        self.video_cap.timer.stop()
        frame_prewiew = self.video_cap.frame_prewiew
        rect = np.zeros_like(frame_prewiew)
        rect = cv2.rectangle(rect, [0, 0], [rect.shape[1], rect.shape[0]], color=(255, 0, 0), thickness=20)
        qimage = QImage(cv2.addWeighted(frame_prewiew, 0.5, rect, 0.5, gamma=1.0), 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(qimage))
        res = calc_contrast(self.video_cap.frame_bw)
        self.view.Contrast_Label.setText(f'{res["contrast"]:.2f}')
        self.video_cap.timer.start()