import sys
import time

import numpy
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import matplotlib.pyplot as plt
import io
from postprocess import postprocess

# from form_tst import Ui_Widget
__RPI__ = False
__PC__ = True
if (__RPI__ == True):
    from picamera2 import Picamera2, Preview
    from picamera2.previews.qt import QGlPicamera2
    from picamera2.controls import Controls
    import pigpio

    pi1 = pigpio.pi()

X_SIZE_IMAGE_RAW_1 = int(2048)
Y_SIZE_IMAGE_RAW_1 = int(1536)

X_SIZE_IMAGE_RAW = int(2048)
Y_SIZE_IMAGE_RAW = int(1536)


class CameraApp(QMainWindow):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 480)
        Widget.setMaximumSize(QtCore.QSize(800, 480))
        self.Img_label = QtWidgets.QLabel(Widget)
        self.Img_label.setGeometry(QtCore.QRect(20, 0, 360, 480))
        self.Img_label.setMaximumSize(QtCore.QSize(480, 720))
        self.Img_label.setFrameShape(QtWidgets.QFrame.Box)
        self.Img_label.setObjectName("Img_label")
        self.tabWidget = QtWidgets.QTabWidget(Widget)
        self.tabWidget.setGeometry(QtCore.QRect(390, 30, 401, 441))
        self.tabWidget.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName("tabWidget")
        self.Measure_page = QtWidgets.QWidget()
        self.Measure_page.setObjectName("Measure_page")
        self.Hist_label = QtWidgets.QLabel(self.Measure_page)
        self.Hist_label.setGeometry(QtCore.QRect(10, 10, 384, 192))
        self.Hist_label.setMinimumSize(QtCore.QSize(256, 192))
        self.Hist_label.setMaximumSize(QtCore.QSize(512, 256))
        self.Hist_label.setFrameShape(QtWidgets.QFrame.Box)
        self.Hist_label.setScaledContents(False)
        self.Hist_label.setObjectName("Hist_label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Measure_page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(6, 320, 381, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Capture_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Capture_pushButton.setFont(font)
        self.Capture_pushButton.setObjectName("Capture_pushButton")
        self.verticalLayout.addWidget(self.Capture_pushButton)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.Measure_page)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 210, 361, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.verticalLayoutWidget_2)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Contrast_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Contrast_label.setFont(font)
        self.Contrast_label.setObjectName("Contrast_label")
        self.gridLayout.addWidget(self.Contrast_label, 0, 0, 1, 1)
        self.Black_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Black_label.setFont(font)
        self.Black_label.setObjectName("Black_label")
        self.gridLayout.addWidget(self.Black_label, 2, 0, 1, 1)
        self.White_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.White_label.setFont(font)
        self.White_label.setObjectName("White_label")
        self.gridLayout.addWidget(self.White_label, 3, 0, 1, 1)
        self.Contrast_draw_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Contrast_draw_label.setFont(font)
        self.Contrast_draw_label.setObjectName("Contrast_draw_label")
        self.gridLayout.addWidget(self.Contrast_draw_label, 0, 1, 1, 1)
        self.Black_level_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Black_level_label.setFont(font)
        self.Black_level_label.setObjectName("Black_level_label")
        self.gridLayout.addWidget(self.Black_level_label, 2, 1, 1, 1)
        self.White_level_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.White_level_label.setFont(font)
        self.White_level_label.setObjectName("White_level_label")
        self.gridLayout.addWidget(self.White_level_label, 3, 1, 1, 1)
        self.tabWidget.addTab(self.Measure_page, "")
        self.Calibration_page = QtWidgets.QWidget()
        self.Calibration_page.setObjectName("Calibration_page")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.Calibration_page)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 19, 381, 231))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Calibrate_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_button.sizePolicy().hasHeightForWidth())
        self.Calibrate_button.setSizePolicy(sizePolicy)
        self.Calibrate_button.setIconSize(QtCore.QSize(16, 16))
        self.Calibrate_button.setObjectName("Calibrate_button")
        self.verticalLayout_3.addWidget(self.Calibrate_button)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.Calibration_label = QtWidgets.QLabel(self.Calibration_page)
        self.Calibration_label.setEnabled(True)
        self.Calibration_label.setGeometry(QtCore.QRect(16, 380, 300, 25))
        self.Calibration_label.setScaledContents(False)
        self.Calibration_label.setObjectName("Calibration_label")
        self.tabWidget.addTab(self.Calibration_page, "")
        self.Control_page = QtWidgets.QWidget()
        self.Control_page.setObjectName("Control_page")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.Control_page)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(60, 50, 271, 141))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.White_horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget_4)
        self.White_horizontalSlider.setTabletTracking(False)
        self.White_horizontalSlider.setMaximum(100)
        self.White_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.White_horizontalSlider.setInvertedAppearance(False)
        self.White_horizontalSlider.setInvertedControls(False)
        self.White_horizontalSlider.setObjectName("White_horizontalSlider")
        self.verticalLayout_4.addWidget(self.White_horizontalSlider)
        self.IR_horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget_4)
        self.IR_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.IR_horizontalSlider.setObjectName("IR_horizontalSlider")
        self.verticalLayout_4.addWidget(self.IR_horizontalSlider)
        self.Mode_radioButton = QtWidgets.QRadioButton(self.Control_page)
        self.Mode_radioButton.setGeometry(QtCore.QRect(10, 250, 301, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mode_radioButton.sizePolicy().hasHeightForWidth())
        self.Mode_radioButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Mode_radioButton.setFont(font)
        self.Mode_radioButton.setIconSize(QtCore.QSize(32, 32))
        self.Mode_radioButton.setObjectName("Mode_radioButton")
        self.label = QtWidgets.QLabel(self.Control_page)
        self.label.setGeometry(QtCore.QRect(0, 70, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Control_page)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Control_page)
        self.label_3.setGeometry(QtCore.QRect(90, 20, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.Control_page, "")
        self.IP_label = QtWidgets.QLabel(Widget)
        self.IP_label.setGeometry(QtCore.QRect(390, 6, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.IP_label.setFont(font)
        self.IP_label.setToolTipDuration(-1)
        self.IP_label.setObjectName("IP_label")
        self.Port_label = QtWidgets.QLabel(Widget)
        self.Port_label.setGeometry(QtCore.QRect(660, 10, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Port_label.setFont(font)
        self.Port_label.setObjectName("Port_label")

        self.retranslateUi(Widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.Img_label.setText(_translate("Widget", " "))
        self.Hist_label.setText(_translate("Widget", " "))
        self.Capture_pushButton.setText(_translate("Widget", "Захват изображения"))
        self.pushButton.setText(_translate("Widget", "Сохранение изображения"))
        self.Contrast_label.setText(_translate("Widget", "Контраст: "))
        self.Black_label.setText(_translate("Widget", "Уровень черного:"))
        self.White_label.setText(_translate("Widget", "Уровень белого:"))
        self.Contrast_draw_label.setText(_translate("Widget", "0.00"))
        self.Black_level_label.setText(_translate("Widget", "0.00"))
        self.White_level_label.setText(_translate("Widget", "0.00"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Measure_page), _translate("Widget", "Измерения"))
        self.Calibrate_button.setText(_translate("Widget", "Калибровка"))
        self.pushButton_3.setText(_translate("Widget", "Восстановить заводскую калибровку"))
        self.Calibration_label.setText(_translate("Widget", "Калибровка успешно завершена"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Calibration_page), _translate("Widget", "Калибровка"))
        self.Mode_radioButton.setText(_translate("Widget", "Режим работы по движению"))
        self.label.setText(_translate("Widget", "VIS"))
        self.label_2.setText(_translate("Widget", "IR"))
        self.label_3.setText(_translate("Widget", "Мощность подсветки "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Control_page), _translate("Widget", "Настройки"))
        self.IP_label.setText(_translate("Widget", "IP: 0.0.0.0"))
        self.Port_label.setText(_translate("Widget", "Port: 00000"))

    def __init__(self):
        super().__init__()

        # Create an instance of the UI
        # self.ui = Ui_Widget()
        self.setupUi(self)
        if (__RPI__ == True):
            pi1.set_mode(16, pigpio.OUTPUT)
            pi1.set_mode(20, pigpio.OUTPUT)
            pi1.set_mode(21, pigpio.OUTPUT)
            pi1.set_mode(26, pigpio.OUTPUT)
            self.camera = Picamera2()

            self.camera.stop()

            config = self.camera.create_still_configuration(
                main={"format": "YUV420", "size": (X_SIZE_IMAGE_RAW_1, Y_SIZE_IMAGE_RAW_1)}, lores=None, raw=None,
                buffer_count=4)
            self.camera.configure(config)
            # set camera settings
            ctrls = Controls(self.camera)
            ctrls.AnalogueGain = 4.0
            ctrls.ExposureTime = 20000
            ctrls.AeEnable = False
            # ctrls.ColourGains = (1.0,1.0)
            # ctrls.AeFlickerMode = Picamera2.FlickerOff
            # ctrls.AfMode = Manual
            ctrls.AwbEnable = False
            ctrls.NoiseReductionMode = False
            self.camera.set_controls(ctrls)
            self.camera.start()
            # set camera settings
            # ctrls = Controls(self.camera)
            # ctrls.AnalogueGain = 4.0
            # ctrls.ExposureTime = 20000
            # ctrls.AeEnable=False
            # ctrls.ColourGains = (1.0,1.0)
            # ctrls.AeFlickerMode = Picamera2.FlickerOff
            # ctrls.AfMode = Manual
            # ctrls.AwbEnable = False
            # ctrls.NoiseReductionMode = False
            # self.camera.set_controls(ctrls)
            # time.sleep(1)
            # get and print sensor mode
            metadata = self.camera.capture_metadata()
            print(metadata)
        self.initUI()
        self.Capture_pushButton.clicked.connect(self.capture_image)

    def initUI(self):
        self.setWindowTitle('Контрастометр')
        self.setGeometry(0, 0, 800, 480)

        # Timer for updating the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # Update every 100 ms (approx. 10 fps)

    def update_frame(self):
        if (__RPI__ == True):
            pi1.write(16, 1)
            if self.camera is None:
                return

        frame = np.zeros((X_SIZE_IMAGE_RAW, Y_SIZE_IMAGE_RAW), dtype=numpy.uint8)
        # Capture a frame from the video stream
        if (__RPI__ == True):
            pi1.write(20, 1)
            frame = self.camera.capture_array("main")
            pi1.write(20, 0)
        if (__PC__ == True):
            frame = np.random.randint(0, 256, size=(X_SIZE_IMAGE_RAW, Y_SIZE_IMAGE_RAW), dtype=np.uint8)

        # copy only gray image, without color
        res = np.resize(frame, (Y_SIZE_IMAGE_RAW, X_SIZE_IMAGE_RAW))

        if (__PC__ == True):
            frame2 = frame.copy()

        # в 4.2667 раза меньше чем для кропа исходника
        # y_size_start = 23
        # y_size_stop  = 328
        # x_size_start = 117
        # x_size_stop  = 352
        # for i in range (x_size_start,x_size_stop,1):
        #    res3[y_size_start,i]=255
        #    res3[y_size_stop,i]=255
        # for i in range(y_size_start,y_size_stop,1):
        #    res3[i,x_size_start]=255
        #    res3[i,x_size_stop]=255

        if __RPI__ == True:
            pi1.write(21, 1)
        # range frame
        x1, x2 = 500, 1500
        y1, y2 = 100, 1400
        img = cv2.rectangle(frame, [x1, y1], [x2, y2], 255, 5)
        # crop for processing, limited rectangle
        crop_img = res[y1:y2, x1:x2]
        if __RPI__ == True:
            pi1.write(21, 0)
            # get RGB frame from YUV420
            frame2 = cv2.cvtColor(img, cv2.COLOR_YUV420p2RGB)
        if __RPI__ == True:
            pi1.write(21, 1)
        # resize frame for display
        frame3 = cv2.resize(frame2, (480, 360))
        # rotate from for display
        res3 = cv2.rotate(frame3, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # resize image for processing, decrease by 2
        # crop_img = cv2.resize(crop_img, ((int(crop_img.shape[1] / 2)), int(crop_img.shape[0] / 2)))
        # computing contrast
        self.result_proc = postprocess(crop_img)
        if __RPI__ == True:
            pi1.write(21, 0)

        if (__RPI__ == True):
            pi1.write(26, 1)
        # display contrast on display

        pass

        if (self.result_proc["contrast"] != None):
            self.Contrast_draw_label.setText("{0:3.3f}".format(self.result_proc["contrast"]))
            self.Black_level_label.setText("{0:3.3f}".format(self.result_proc["avg_numbers"]))
            self.White_level_label.setText("{0:3.3f}".format(self.result_proc["avg_paper"]))
        # create Qimage
        self.qimage = QImage(res3, 360, 480, 360, QImage.Format_Indexed8)
        self.qimage2 = QImage(self.result_proc["histogram"], 384, 192, 384*3, QImage.Format_RGB888)
        # display images
        self.Img_label.setPixmap(QPixmap.fromImage(self.qimage))
        self.Hist_label.setPixmap(QPixmap.fromImage(self.qimage2))

        if (__RPI__ == True):
            pi1.write(26, 0)
            pi1.write(16, 0)
            # self.Hist_label.setPixmap(QPixmap.fromImage(self.qimage2))

    def capture_image(self):
        if (__RPI__ == True):
            # Capture the current frame from the video stream
            if self.camera is None:
                print("Camera not initialized.")
                return
        elif (__PC__ == True):
            pass

    def save_image(self):
        # Save the image to a file
        return

    def IR_control(self):
        if (self.checkBox_IR.isChecked() == True):
            print("press IR\r\n")
        if (self.checkBox_IR.isChecked() == False):
            print("release IR\r\n")
        return

    def White_control(self):
        if (self.checkBox_White.isChecked() == True):
            print("press White\r\n")
        if (self.checkBox_White.isChecked() == False):
            print("release White\r\n")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    ex.show()
    sys.exit(app.exec_())
