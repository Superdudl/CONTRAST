import numpy as np
from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QImage, QPixmap


class VideoCapture(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None
        self.update_frame()

    def update_frame(self):
        self.frame = np.random.randint(0, 255, (480, 360, 3), dtype=np.uint8)
        self.qimage = QImage(self.frame, 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
