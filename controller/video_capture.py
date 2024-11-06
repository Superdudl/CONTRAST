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

        self.lookUpTable = np.empty((1,256), np.uint8)
        for i in range(256):
            self.lookUpTable[0,i] = np.clip(pow(i / 255.0, 1.4) * 255.0, 0, 255)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None
        self.gain = None
        self.prev_frame = None
        self.frame_preview = None
        self.crosshair = ((135, 585), (1935, 945))
        self.setupUI()
        self.update_frame()

    def setupUI(self):
        self.view.tabWidget.currentChanged.connect(self.change_crosshair)

    def change_crosshair(self, index):
        if index == 0:
            self.crosshair = ((135, 585), (1935, 945))
        elif index == 1:
            self.crosshair = ((964, 708),(1084, 828))


    def update_frame(self):
        if platform.system() == 'Windows':
            self.prev_frame = self.frame_preview
            self.frame = np.random.randint(0, 255, (1536, 2048, 3), dtype=np.uint8)
            self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
            frame = cv2.rectangle(self.frame, self.crosshair[0], self.crosshair[1], (255, 255, 255), 10)
            # self.frame = np.random.randint(0, 1, (480, 360, 3), dtype=np.uint8)
            self.frame_preview = cv2.resize(frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            self.prev_frame = self.frame_preview
            self.frame = self.camera.capture_array('main')
            self.frame_bw_orig = self.frame[0:self.h, 0:self.w].copy()
            self.frame_bw = self.frame_bw_orig.copy()
            if self.gain is not None:
                self.frame_bw = np.float32(self.frame_bw)
                self.frame_bw *= self.gain
                self.frame_bw = np.uint8(self.frame_bw)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_YUV420p2BGR)
            frame = cv2.rectangle(self.frame, self.crosshair[0], self.crosshair[1], (255, 255, 255), 10)
            self.frame_preview = cv2.resize(self.frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)

        self.qimage = QImage(self.frame_preview, 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        return
