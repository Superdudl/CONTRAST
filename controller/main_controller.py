from PyQt5.QtCore import QObject
from controller import CalibrationController, VideoCapture, ParamsController, MeasureController


class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.connect_controllers()

    def connect_controllers(self):
        self.calibration_controller = CalibrationController(self.view)
        self.video_capture = VideoCapture(self.view)
        self.params_controller = ParamsController(self.view, self.video_capture)
        self.measure_controller = MeasureController(self.view, self.video_capture)
