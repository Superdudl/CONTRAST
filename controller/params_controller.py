from PyQt5.QtCore import QObject
from PyQt5 import QtGui, QtCore

class ParamsController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setupUI()

    def setupUI(self):
        self.view.Apply_capture_image_pushButton.clicked.connect(self.apply_img_capture_params)

    def apply_img_capture_params(self):
        if self.view.EN_Hist_checkBox.isChecked():
            self.view.Hist_Label.show()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(50, 240, 300, 120))
            font = QtGui.QFont()
            font.setPointSize(30)
            self.view.Contrast_Label.setFont(font)
        else:
            self.view.Hist_Label.hide()
            self.view.Contrast_Label.setGeometry(QtCore.QRect(50, 130, 300, 120))
            font = QtGui.QFont()
            font.setPointSize(100)
            self.view.Contrast_Label.setFont(font)

