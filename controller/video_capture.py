import numpy as np
from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QImage, QPixmap
import platform
import json


class VideoCapture(QObject):
    def __init__(self, view):
        super().__init__()
        self.camera = None
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None
        self.update_frame()

    def update_frame(self):
        if platform.system() == 'Windows':
            self.frame = np.random.randint(0, 255, (480, 360, 3), dtype=np.uint8)
        else:
            from picamera2 import Picamera2, Preview
            from picamera2.previews.qt import QGlPicamera2
            from picamera2.controls import Controls
            import pigpio

            self.camera = Picamera2()
            config = self.camera.create_still_configuration(
                main={"format": "YUV420", "size": (X_SIZE_IMAGE_RAW_1, Y_SIZE_IMAGE_RAW_1)}, lores=None, raw=None,
                buffer_count=4)
            self.camera.configure(config)
            with open(r'../src/camera_config.json', 'r') as json_file:
                self.ctrls = json.load(json_file)
            self.camera.set_controls(self.ctrls)
            self.camera.start()
            metadata = self.camera.capture_metadata()
            print(metadata)

        self.qimage = QImage(self.frame, 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
