import cv2
import numpy as np
from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QImage, QPixmap
import platform
import json
from pathlib import Path, PurePath
from utils import calibrate


class VideoCapture(QObject):
    def __init__(self, view):
        super().__init__()
        # Проверяем и загружаем файл каллибровки

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

        gray_templates_file = PurePath(Path(__file__).parent.parent, 'src', 'calib', 'gray_templates.npy')
        factory_gray_templates_file = PurePath(Path(__file__).parent.parent, 'src', 'calib',
                                               'factory_gray_templates.npy')
        if Path(gray_templates_file).exists():
            self.gray_templates = np.load(Path(gray_templates_file))
        elif Path(factory_gray_templates_file).exists():
            self.gray_templates = np.load(Path(factory_gray_templates_file))
        else:
            self.gray_templates = None

        with open(str(PurePath(Path(__file__).parent.parent, 'src', 'camera_config.json')), 'r') as json_file:
            self.ctrls = json.load(json_file)
            self.ctrls['AnalogueGain'] = int(self.ctrls['AnalogueGain'])
            self.ctrls['ExposureTime'] = int(self.ctrls['ExposureTime'])
        self.scale = 1.8
        self.h, self.w = int(1536 / self.scale), int(2048 / self.scale)
        if platform.system() != 'Windows':
            from picamera2 import Picamera2, Preview
            from picamera2.previews.qt import QGlPicamera2
            from picamera2.controls import Controls
            import pigpio

            tuning = Picamera2.load_tuning_file(str(PurePath(Path(__file__).parent.parent, "src", "imx219.json")))

            self.camera = Picamera2(tuning=tuning)
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

        # Координаты прямоугольной рамки
        self._x1, self._x2 = 48, 2000
        self._y1, self._y2 = 585, 945
        self.crosshair = (
            (int(self._x1 / self.scale), int(self._y1 / self.scale)),
            (int(self._x2 / self.scale), int(self._y2 / self.scale)))
        self.calib_obj_crosshair = (
            (int(410 / self.scale), int(350 / self.scale)),
            (int(410 / self.scale), int(1250 / self.scale)),
            40)  # [center1, center2, radius]

        self.setupUI()
        self.update_frame()

    def setupUI(self):
        self.view.tabWidget.currentChanged.connect(self.change_crosshair)

    def change_crosshair(self, index):
        if index == 0:
            self.crosshair = (
                (int(48 / self.scale), int(585 / self.scale)), (int(2000 / self.scale), int(945 / self.scale)))
        elif index == 1:
            self.crosshair = (
                (int(350 / self.scale), int(708 / self.scale)), (int(470 / self.scale), int(828 / self.scale)))

    def update_frame(self, update_preview=True):
        def update_LUT():
            nominal_obj_1 = self.gray_templates[0]
            nominal_obj_2 = self.gray_templates[1]
            x1_1 = int(self.calib_obj_crosshair[0][0] - self.calib_obj_crosshair[2] / 1.42)
            x1_2 = int(self.calib_obj_crosshair[0][0] + self.calib_obj_crosshair[2] / 1.42)
            x2_1 = int(self.calib_obj_crosshair[1][0] - self.calib_obj_crosshair[2] / 1.42)
            x2_2 = int(self.calib_obj_crosshair[1][0] + self.calib_obj_crosshair[2] / 1.42)
            y1_1 = int(self.calib_obj_crosshair[0][1] - self.calib_obj_crosshair[2] / 1.42)
            y1_2 = int(self.calib_obj_crosshair[0][1] + self.calib_obj_crosshair[2] / 1.42)
            y2_1 = int(self.calib_obj_crosshair[1][1] - self.calib_obj_crosshair[2] / 1.42)
            y2_2 = int(self.calib_obj_crosshair[1][1] + self.calib_obj_crosshair[2] / 1.42)
            ADC_obj_1 = np.mean(self.frame_bw_orig[y1_1:y1_2, x1_1:x1_2]) * 1.5
            ADC_obj_2 = np.mean(self.frame_bw_orig[y2_1:y2_2, x2_1:x2_2]) * 1.5
            self.calib_LUT = calibrate([ADC_obj_1, ADC_obj_2], [nominal_obj_1, nominal_obj_2], gray_templates=True)

        if platform.system() == 'Windows':
            self.prev_frame = self.frame_preview
            self.frame = np.random.randint(0, 255, (self.h, self.w, 3), dtype=np.uint8)
            self.frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
            self.frame_bw_orig = self.frame_bw.copy()
            if self.gray_templates is not None:
                update_LUT()
            frame = cv2.rectangle(self.frame, self.crosshair[0], self.crosshair[1], (255, 255, 255), 6)
            frame = cv2.circle(frame, self.calib_obj_crosshair[0], self.calib_obj_crosshair[2], (255, 255, 255), 6)
            frame = cv2.circle(frame, self.calib_obj_crosshair[1], self.calib_obj_crosshair[2], (255, 255, 255), 6)
            self.frame_preview = cv2.resize(frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            # Получение изображения с камеры
            self.prev_frame = self.frame_preview  # Предыдущий кадр
            self.frame = self.camera.capture_array('main')  # Новый кадр
            self.orig_frame = self.frame.copy()  # Храним оригинальный кадр без обработки
            self.frame_bw_orig = self.frame[:, :, 0].copy()  # Храним оригинальный ч-б кадр без обработки

            x1, y1 = int(self._x1 / self.scale), int(self._y1 / self.scale)
            x2, y2 = int(self._x2 / self.scale), int(self._y2 / self.scale)

            if self.dark is not None:
                self.frame = cv2.subtract(self.orig_frame, self.dark)
            if self.gain is not None:
                self.frame = np.float32(self.frame)
                self.frame[y1:y2, x1:x2] = cv2.multiply(self.frame[y1:y2, x1:x2], self.gain[y1:y2, x1:x2])
                self.frame[y1:y2, x1:x2] = np.clip(self.frame[y1:y2, x1:x2], 0, 255)
                self.frame = np.uint8(self.frame)
            self.frame_bw = self.frame[:, :, 0].copy()
            self.frame_bw_noLUT = self.frame_bw.copy()
            if self.gray_templates is not None:
                update_LUT()
            if self.calib_LUT is not None:
                self.frame_bw[y1:y2, x1:x2] = cv2.LUT(self.frame_bw[y1:y2, x1:x2], self.calib_LUT)

            frame = cv2.rectangle(self.frame.copy(), self.crosshair[0], self.crosshair[1], (255, 255, 255), 6)
            frame = cv2.circle(frame, self.calib_obj_crosshair[0], self.calib_obj_crosshair[2], (255, 255, 255), 6)
            frame = cv2.circle(frame, self.calib_obj_crosshair[1], self.calib_obj_crosshair[2], (255, 255, 255), 6)
            self.frame_preview = cv2.resize(frame, (480, 360))
            self.frame_preview = cv2.rotate(self.frame_preview, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if update_preview:
            self.qimage = QImage(self.frame_preview, 360, 480, 360 * 3, QImage.Format_RGB888)
            self.view.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        return
