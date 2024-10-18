import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from utils import histogram
from view import CameraApp


class VideoCapture:
    def __init__(self, view):
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None

    def update_frame(self):
        self.frame = np.random.randint(0, 255, (480, 360, 3), dtype=np.uint8)
        self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        hist = histogram(self.frame_bw)
        self.qimage = QImage(self.frame, 360, 480, 360 * 3, QImage.Format_RGB888)
        # self.qimage2 = QImage(hist, 384, 192, 384 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        # self.view.Hist_Label.setPixmap(QPixmap.fromImage(self.qimage2))
