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

        # Измерение
        self.view.Measure_pushButton.clicked.connect(self.calc_contrast)

    def calc_hist(self):
        self.frame = self.video_cap.frame_bw
        self.hist = histogram(self.frame)
        self.qimage = QImage(self.hist, 384, 192, 384 * 3, QImage.Format_RGB888)
        self.view.Hist_Label.setPixmap(QPixmap.fromImage(self.qimage))

    def calc_contrast(self):
        self.video_cap.timer.stop()
        frame_prewiew = self.video_cap.frame_preview
        rect = np.zeros_like(frame_prewiew)
        rect = cv2.rectangle(rect, [0, 0], [rect.shape[1], rect.shape[0]], color=(255, 0, 0), thickness=20)
        qimage = QImage(cv2.addWeighted(frame_prewiew, 0.5, rect, 0.5, gamma=1.0), 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(qimage))
        res = calc_contrast(self.video_cap.frame_bw)
        if res["contrast"] is not None:
            self.view.Contrast_Label.setText(f'{res["contrast"]:.2f}')
        self.video_cap.timer.start()

    def motion_detector(self):
        if self.video_cap.prev_frame is not None:
            curr = cv2.cvtColor(self.video_cap.frame_preview, cv2.COLOR_RGB2GRAY)
            curr = cv2.GaussianBlur(curr, (21, 21), 3)

            try:
                prev = cv2.cvtColor(self.video_cap.prev_frame, cv2.COLOR_RGB2GRAY)
                prev = cv2.GaussianBlur(prev, (21, 21), 3)
            except cv2.error as e:
                prev = np.zeros_like(curr)
            diff = cv2.absdiff(prev, curr)
            if diff[diff < 2] / len(diff) > 0.995:
                self.calc_contrast()

