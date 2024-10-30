from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore
from controller import CalibrationController, VideoCapture, ParamsController, MeasureController


class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setupUI()
        self.connect_controllers()

    def setupUI(self):
        self.view.Hist_Widget.hide()
        self.view.Contrast_Label.setGeometry(QtCore.QRect(75, 130, 300, 140))
        font = QtGui.QFont()
        font.setPointSize(100)
        self.view.Contrast_Label.setFont(font)
        self.view.Contrast_Label.setText("0,00")

    def connect_controllers(self):
        self.calibration_controller = CalibrationController(self.view)
        self.video_capture = VideoCapture(self.view)
        self.measure_controller = MeasureController(self.view, self.video_capture)
        self.params_controller = ParamsController(self.view, self.video_capture, self.measure_controller)
