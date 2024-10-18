from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QImage, QPixmap
from utils import histogram
import numpy as np
import cv2

class MeasureController(QObject):
    def __init__(self, view, video_cap):
        super().__init__()
        self.video_cap = video_cap
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.calc_hist)
        self.timer.start(100)
        self.calc_hist()

    def calc_hist(self):
        self.frame = self.video_cap.frame
        self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        self.hist = histogram(self.frame_bw)
        self.qimage = QImage(self.hist, 384, 192, 384 * 3, QImage.Format_RGB888)
        self.view.Hist_Label.setPixmap(QPixmap.fromImage(self.qimage))
