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
        # Проверяем и загружаем файл каллибровки

        calib_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'calib_config.npy')
        factory_calib_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_calib_config.npy')
        if Path(calib_file).exists():
            self.calib_LUT = np.load(Path(calib_file))
        elif Path(factory_calib_file).exists():
            self.calib_LUT = np.load(Path(factory_calib_file))
        else:
            self.calib_LUT = None

        gain_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gain_config.npy')
        factory_gain_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_gain_config.npy')
        if Path(gain_file).exists():
            self.gain = np.load(Path(gain_file))
        elif Path(factory_gain_file).exists():
            self.gain = np.load(Path(factory_gain_file))
        else:
            self.gain = None

        dark_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'dark_config.npy')
        factory_dark_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'factory_dark_config.npy')
        if Path(dark_file).exists():
            self.dark = np.load(Path(dark_file))
        elif Path(factory_dark_file).exists():
            self.dark = np.load(Path(factory_dark_file))
        else:
            self.dark = None

        with open(str(PurePath(Path(__file__).parent.parent, 'src', 'camera_config.json')), 'r') as json_file:
            self.ctrls = json.load(json_file)
            self.ctrls['AnalogueGain'] = int(self.ctrls['AnalogueGain'])
            self.ctrls['ExposureTime'] = int(self.ctrls['ExposureTime'])
        self.scale = 1.8
        if platform.system() != 'Windows':
            from picamera2 import Picamera2, Preview
            from picamera2.previews.qt import QGlPicamera2
            from picamera2.controls import Controls
            import pigpio

            tuning = Picamera2.load_tuning_file(str(PurePath(Path(__file__).parent.parent, "src", "imx219.json")))

            self.camera = Picamera2(tuning=tuning)
            self.h, self.w = int(1536/self.scale), int(2048/self.scale)
            config = self.camera.create_still_configuration(
                main={"format": "BGR888", "size": (self.w, self.h)}, lores=None, raw=None,
                buffer_count=4)
            self.camera.configure(config)
            self.camera.set_controls(self.ctrls)
            self.camera.start()
            metadata = self.camera.capture_metadata()
            print(metadata)

        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.frame = None
        self.prev_frame = None
        self.frame_preview = None
        self.crosshair = ((int(135/self.scale), int(585/self.scale)), (int(1935/self.scale), int(945/self.scale)))
        self.setupUI()
        self.update_frame()

    def setupUI(self):
        self.view.tabWidget.currentChanged.connect(self.change_crosshair)

    def change_crosshair(self, index):
        if index == 0:
            self.crosshair = ((int(135/self.scale), int(585/self.scale)), (int(1935/self.scale), int(945/self.scale)))
        elif index == 1:
            self.crosshair = ((int(964/self.scale), int(708/self.scale)), (int(1084/self.scale), int(828/self.scale)))

    def update_frame(self):
        if platform.system() == 'Windows':
            self.prev_frame = self.frame_preview
            self.frame = np.random.randint(0, 255, (1536, 2048, 3), dtype=np.uint8)
            self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
            self.frame_bw_orig = self.frame_bw.copy()
            frame = cv2.rectangle(self.frame, self.crosshair[0], self.crosshair[1], (255, 255, 255), 10)
            # self.frame = np.random.randint(0, 1, (480, 360, 3), dtype=np.uint8)
            self.frame_preview = cv2.resize(frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            self.prev_frame = self.frame_preview
            self.frame = self.camera.capture_array('main')
            self.orig_frame = self.frame.copy()
            if self.dark is not None:
                cv2.subtract(self.orig_frame, self.dark, self.frame)
            if self.gain is not None:
                self.frame = np.float32(self.frame)
                # self.frame *= self.gain
                cv2.multiply(self.frame, self.gain, dst=self.frame)
                self.frame = np.clip(self.frame, 0, 255)
                self.frame = np.uint8(self.frame)
            self.frame_bw_orig = self.frame[:, :, 0].copy()
            self.frame_bw = self.frame_bw_orig.copy()
            if self.calib_LUT is not None:
                cv2.LUT(self.frame_bw, self.calib_LUT, self.frame_bw)
            # frame = cv2.cvtColor(self.frame, cv2.COLOR_YUV420p2BGR).copy()
    
            frame = cv2.rectangle(self.frame.copy(), self.crosshair[0], self.crosshair[1], (255, 255, 255), 6)
            self.frame_preview = cv2.resize(frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)

        self.qimage = QImage(self.frame_preview, 360, 480, 360 * 3, QImage.Format_RGB888)
        self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        return
