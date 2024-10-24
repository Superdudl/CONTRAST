import cv2
import numpy as np
from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QImage, QPixmap
import platform
import json
from pathlib import Path, PurePath


class VideoCapture(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        if platform.system() != 'Windows':
            from picamera2 import Picamera2, Preview
            from picamera2.previews.qt import QGlPicamera2
            from picamera2.controls import Controls
            import pigpio

            tuning = Picamera2.load_tuning_file(str(PurePath(Path(__file__).parent.parent, "src", "imx219.json")))

            self.camera = Picamera2(tuning=tuning)
            self.h, self.w = 1536, 2048
            config = self.camera.create_still_configuration(
                main={"format": "YUV420", "size": (self.w, self.h)}, lores=None, raw=None,
                buffer_count=4)
            self.camera.configure(config)

            with open(str(PurePath(Path(__file__).parent.parent, 'src', 'camera_config.json')), 'r') as json_file:
                self.ctrls = json.load(json_file)
                self.ctrls['AnalogueGain'] = int(self.ctrls['AnalogueGain'])
                self.ctrls['ExposureTime'] = int(self.ctrls['ExposureTime'])

            self.camera.set_controls(self.ctrls)
            self.camera.start()
            metadata = self.camera.capture_metadata()
            print(metadata)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None
        self.prev_frame = None
        self.frame_preview = None
        self.update_frame()

    def update_frame(self):
        if platform.system() == 'Windows':
            self.prev_frame = self.frame_preview
            # self.frame = np.random.randint(0, 255, (2048, 1536, 3), dtype=np.uint8)
            self.frame = np.ones(shape=(2048, 1536, 3), dtype=np.uint8)
            self.frame_preview = cv2.resize(self.frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        else:
            self.prev_frame = self.frame_preview
            self.frame = self.camera.capture_array('main')
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_YUV420p2BGR)
            self.frame_preview = cv2.resize(self.frame, (480, 360))
            self.frame_prewiew = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)

        self.qimage = QImage(self.frame_preview, 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        return
