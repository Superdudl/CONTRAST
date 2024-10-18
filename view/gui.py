from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow

__PC__ = True
__RPI__ = False


class CameraApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 480)
        Widget.setMaximumSize(QtCore.QSize(800, 480))
        self.Img_label = QtWidgets.QLabel(Widget)
        self.Img_label.setGeometry(QtCore.QRect(20, 0, 360, 480))
        self.Img_label.setMaximumSize(QtCore.QSize(480, 720))
        self.Img_label.setFrameShape(QtWidgets.QFrame.Box)
        self.Img_label.setText("")
        self.Img_label.setObjectName("Img_label")
        self.tabWidget = QtWidgets.QTabWidget(Widget)
        self.tabWidget.setGeometry(QtCore.QRect(390, 10, 401, 461))
        self.tabWidget.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName("tabWidget")
        self.Measure_page = QtWidgets.QWidget()
        self.Measure_page.setObjectName("Measure_page")
        self.Hist_Label = QtWidgets.QLabel(self.Measure_page)
        self.Hist_Label.setGeometry(QtCore.QRect(10, 10, 384, 192))
        self.Hist_Label.setMinimumSize(QtCore.QSize(384, 192))
        self.Hist_Label.setMaximumSize(QtCore.QSize(512, 256))
        self.Hist_Label.setFrameShape(QtWidgets.QFrame.Box)
        self.Hist_Label.setText("")
        self.Hist_Label.setScaledContents(False)
        self.Hist_Label.setObjectName("Hist_Label")
        self.Contrast_Label = QtWidgets.QLabel(self.Measure_page)
        self.Contrast_Label.setGeometry(QtCore.QRect(150, 240, 131, 81))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.Contrast_Label.setFont(font)
        self.Contrast_Label.setText("0.00")
        self.Contrast_Label.setObjectName("Contrast_Label")
        self.Measure_pushButton = QtWidgets.QPushButton(self.Measure_page)
        self.Measure_pushButton.setEnabled(True)
        self.Measure_pushButton.setGeometry(QtCore.QRect(10, 362, 371, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Measure_pushButton.setFont(font)
        self.Measure_pushButton.setIconSize(QtCore.QSize(21, 16))
        self.Measure_pushButton.setObjectName("Measure_pushButton")
        self.tabWidget.addTab(self.Measure_page, "")
        self.Calibration_page = QtWidgets.QWidget()
        self.Calibration_page.setObjectName("Calibration_page")

        self.Mera_number_label = QtWidgets.QLabel(self.Calibration_page)
        self.Mera_number_label.setGeometry(QtCore.QRect(10, 210, 150, 50))
        self.Mera_number_label.setObjectName("Mera_number_label")
        self.Mera_number_lineEdit = QtWidgets.QLineEdit(self.Calibration_page)
        self.Mera_number_lineEdit.setGeometry(QtCore.QRect(210, 210, 100, 50))
        self.Mera_number_lineEdit.setMaxLength(3)
        self.Mera_number_lineEdit.setReadOnly(True)
        self.Mera_number_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Mera_number_lineEdit.setObjectName("Mera_number_lineEdit")

        self.Nominal_lineEdit = QtWidgets.QLineEdit(self.Calibration_page)
        self.Nominal_lineEdit.setGeometry(QtCore.QRect(210, 80, 100, 50))
        self.Nominal_lineEdit.setMaxLength(3)
        self.Nominal_lineEdit.setReadOnly(True)
        self.Nominal_lineEdit.setObjectName("Nominal_lineEdit")

        self.Nominal_label = QtWidgets.QLabel(self.Calibration_page)
        self.Nominal_label.setGeometry(QtCore.QRect(10, 80, 150, 50))
        self.Nominal_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Nominal_label.setObjectName("Nominal_label")

        self.Measure_mera_label = QtWidgets.QLabel(self.Calibration_page)
        self.Measure_mera_label.setGeometry(QtCore.QRect(10, 140, 150, 50))
        self.Measure_mera_label.setObjectName("Measure_mera_label")
        self.Mera_number_plus_pushButton = QtWidgets.QPushButton(self.Calibration_page)
        self.Mera_number_plus_pushButton.setGeometry(QtCore.QRect(320, 210, 50, 50))
        self.Mera_number_plus_pushButton.setObjectName("Mera_number_plus_pushButton")
        self.Nominal_plus_pushButton = QtWidgets.QPushButton(self.Calibration_page)
        self.Nominal_plus_pushButton.setGeometry(QtCore.QRect(320, 80, 50, 50))
        self.Nominal_plus_pushButton.setObjectName("Nominal_plus_pushButton")
        self.Nominal_minus_pushButton = QtWidgets.QPushButton(self.Calibration_page)
        self.Nominal_minus_pushButton.setGeometry(QtCore.QRect(150, 80, 50, 50))
        self.Nominal_minus_pushButton.setObjectName("Nominal_minus_pushButton")
        self.Mera_number_minus_pushButton = QtWidgets.QPushButton(self.Calibration_page)
        self.Mera_number_minus_pushButton.setGeometry(QtCore.QRect(150, 210, 50, 50))
        self.Mera_number_minus_pushButton.setObjectName("Mera_number_minus_pushButton")
        self.Text_calibrate_page_label = QtWidgets.QLabel(self.Calibration_page)
        self.Text_calibrate_page_label.setGeometry(QtCore.QRect(20, 30, 300, 50))
        self.Text_calibrate_page_label.setObjectName("Text_calibrate_page_label")
        self.Mera_num_max_label = QtWidgets.QLabel(self.Calibration_page)
        self.Mera_num_max_label.setGeometry(QtCore.QRect(320, 30, 50, 50))
        self.Mera_num_max_label.setObjectName("Mera_num_max_label")
        self.Measure_mera_lineEdit = QtWidgets.QLineEdit(self.Calibration_page)
        self.Measure_mera_lineEdit.setGeometry(QtCore.QRect(210, 140, 100, 50))
        self.Measure_mera_lineEdit.setText("")
        self.Measure_mera_lineEdit.setMaxLength(3)
        self.Measure_mera_lineEdit.setReadOnly(True)
        self.Measure_mera_lineEdit.setObjectName("Measure_mera_lineEdit")
        self.gridLayoutWidget = QtWidgets.QWidget(self.Calibration_page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 290, 391, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Mera_push_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mera_push_pushButton.sizePolicy().hasHeightForWidth())
        self.Mera_push_pushButton.setSizePolicy(sizePolicy)
        self.Mera_push_pushButton.setObjectName("Mera_push_pushButton")
        self.gridLayout.addWidget(self.Mera_push_pushButton, 2, 0, 1, 1)
        self.Mera_delete_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mera_delete_pushButton.sizePolicy().hasHeightForWidth())
        self.Mera_delete_pushButton.setSizePolicy(sizePolicy)
        self.Mera_delete_pushButton.setObjectName("Mera_delete_pushButton")
        self.gridLayout.addWidget(self.Mera_delete_pushButton, 2, 2, 1, 1)
        self.Calibrate_start_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_start_pushButton.sizePolicy().hasHeightForWidth())
        self.Calibrate_start_pushButton.setSizePolicy(sizePolicy)
        self.Calibrate_start_pushButton.setObjectName("Calibrate_start_pushButton")
        self.gridLayout.addWidget(self.Calibrate_start_pushButton, 3, 0, 1, 1)
        self.Calibrate_save_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_save_pushButton.sizePolicy().hasHeightForWidth())
        self.Calibrate_save_pushButton.setSizePolicy(sizePolicy)
        self.Calibrate_save_pushButton.setObjectName("Calibrate_save_pushButton")
        self.gridLayout.addWidget(self.Calibrate_save_pushButton, 3, 2, 1, 1)
        self.tabWidget.addTab(self.Calibration_page, "")
        self.Control_page = QtWidgets.QWidget()
        self.Control_page.setObjectName("Control_page")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Control_page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 9, 401, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Control_tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control_tabWidget.sizePolicy().hasHeightForWidth())
        self.Control_tabWidget.setSizePolicy(sizePolicy)
        self.Control_tabWidget.setMouseTracking(False)
        self.Control_tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.Control_tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.Control_tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.Control_tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.Control_tabWidget.setUsesScrollButtons(False)
        self.Control_tabWidget.setObjectName("Control_tabWidget")
        self.User_tab = QtWidgets.QWidget()
        self.User_tab.setObjectName("User_tab")
        self.User_settings_image_toolBox = QtWidgets.QToolBox(self.User_tab)
        self.User_settings_image_toolBox.setGeometry(QtCore.QRect(8, 12, 381, 250))
        self.User_settings_image_toolBox.setObjectName("User_settings_image_toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 381, 335))
        self.page.setObjectName("page")
        self.Capture_image_checkBox = QtWidgets.QCheckBox(self.page)
        self.Capture_image_checkBox.setGeometry(QtCore.QRect(30, 20, 310, 50))
        self.Capture_image_checkBox.setObjectName("Capture_image_checkBox")
        self.EN_Hist_checkBox = QtWidgets.QCheckBox(self.page)
        self.EN_Hist_checkBox.setGeometry(QtCore.QRect(30, 50, 310, 50))
        self.EN_Hist_checkBox.setObjectName("EN_Hist_checkBox")
        self.Apply_capture_image_pushButton = QtWidgets.QPushButton(self.page)
        self.Apply_capture_image_pushButton.setGeometry(QtCore.QRect(100, 120, 180, 50))
        self.Apply_capture_image_pushButton.setObjectName("Apply_capture_image_pushButton")

        self.page_base_calibr = QtWidgets.QWidget()
        self.page_base_calibr.setObjectName("page_base_calibr")
        self.User_settings_image_toolBox.addItem(self.page, "")
        self.User_settings_image_toolBox.addItem(self.page_base_calibr, '')

        self.Control_tabWidget.addTab(self.User_tab, "Пользовательские")
        self.tab_service = QtWidgets.QWidget()
        self.tab_service.setObjectName("tab_service")
        self.toolBox = QtWidgets.QToolBox(self.tab_service)
        self.toolBox.setGeometry(QtCore.QRect(10, 10, 371, 381))
        self.toolBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox.setObjectName("toolBox")
        self.page_led = QtWidgets.QWidget()
        self.page_led.setGeometry(QtCore.QRect(0, 0, 371, 273))
        self.page_led.setObjectName("page_led")
        self.White_LED_minus_pushButton = QtWidgets.QPushButton(self.page_led)
        self.White_LED_minus_pushButton.setGeometry(QtCore.QRect(100, 50, 50, 50))
        self.White_LED_minus_pushButton.setObjectName("White_LED_minus_pushButton")
        self.IR_LED_minus_pushButton = QtWidgets.QPushButton(self.page_led)
        self.IR_LED_minus_pushButton.setGeometry(QtCore.QRect(100, 110, 50, 50))
        self.IR_LED_minus_pushButton.setObjectName("IR_LED_minus_pushButton")
        self.White_LED_plus_pushButton = QtWidgets.QPushButton(self.page_led)
        self.White_LED_plus_pushButton.setGeometry(QtCore.QRect(230, 50, 50, 50))
        self.White_LED_plus_pushButton.setObjectName("White_LED_plus_pushButton")
        self.IR_LED_plus_pushButton = QtWidgets.QPushButton(self.page_led)
        self.IR_LED_plus_pushButton.setGeometry(QtCore.QRect(230, 110, 50, 50))
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.IR_LED_plus_pushButton.setFont(font)
        self.IR_LED_plus_pushButton.setObjectName("IR_LED_plus_pushButton")
        self.Apply_LED_pushButton = QtWidgets.QPushButton(self.page_led)
        self.Apply_LED_pushButton.setGeometry(QtCore.QRect(100, 190, 180, 50))
        self.Apply_LED_pushButton.setAutoDefault(False)
        self.Apply_LED_pushButton.setDefault(False)
        self.Apply_LED_pushButton.setFlat(False)
        self.Apply_LED_pushButton.setObjectName("Apply_LED_pushButton")
        self.White_LED_label = QtWidgets.QLabel(self.page_led)
        self.White_LED_label.setGeometry(QtCore.QRect(10, 50, 60, 50))
        self.White_LED_label.setObjectName("White_LED_label")
        self.IR_LED_label = QtWidgets.QLabel(self.page_led)
        self.IR_LED_label.setGeometry(QtCore.QRect(10, 110, 60, 50))
        self.IR_LED_label.setObjectName("IR_LED_label")
        self.White_LED_lineEdit = QtWidgets.QLineEdit(self.page_led)
        self.White_LED_lineEdit.setGeometry(QtCore.QRect(155, 50, 70, 50))
        self.White_LED_lineEdit.setMaxLength(3)
        self.White_LED_lineEdit.setReadOnly(True)
        self.White_LED_lineEdit.setObjectName("White_LED_lineEdit")
        self.IR_LED_lineEdit = QtWidgets.QLineEdit(self.page_led)
        self.IR_LED_lineEdit.setGeometry(QtCore.QRect(155, 110, 70, 50))
        self.IR_LED_lineEdit.setMaxLength(3)
        self.IR_LED_lineEdit.setReadOnly(True)
        self.IR_LED_lineEdit.setObjectName("IR_LED_lineEdit")
        self.White_LED_minus_pushButton.raise_()
        self.IR_LED_minus_pushButton.raise_()
        self.White_LED_plus_pushButton.raise_()
        self.IR_LED_plus_pushButton.raise_()
        self.Apply_LED_pushButton.raise_()
        self.IR_LED_label.raise_()
        self.White_LED_lineEdit.raise_()
        self.IR_LED_lineEdit.raise_()
        self.White_LED_label.raise_()
        self.toolBox.addItem(self.page_led, "")
        self.page_cam = QtWidgets.QWidget()
        self.page_cam.setGeometry(QtCore.QRect(0, 0, 371, 273))
        self.page_cam.setObjectName("page_cam")
        self.Exposition_lineEdit = QtWidgets.QLineEdit(self.page_cam)
        self.Exposition_lineEdit.setGeometry(QtCore.QRect(155, 80, 70, 50))
        self.Exposition_lineEdit.setMaxLength(3)
        self.Exposition_lineEdit.setObjectName("Exposition_lineEdit")
        self.Exposition_minus_pushButton = QtWidgets.QPushButton(self.page_cam)
        self.Exposition_minus_pushButton.setGeometry(QtCore.QRect(100, 80, 50, 50))
        self.Exposition_minus_pushButton.setObjectName("Exposition_minus_pushButton")
        self.Exposition_plus_pushButton = QtWidgets.QPushButton(self.page_cam)
        self.Exposition_plus_pushButton.setGeometry(QtCore.QRect(230, 80, 50, 50))
        self.Exposition_plus_pushButton.setObjectName("Exposition_plus_pushButton")
        self.Exposition_Apply_pushButton = QtWidgets.QPushButton(self.page_cam)
        self.Exposition_Apply_pushButton.setGeometry(QtCore.QRect(100, 170, 180, 50))
        self.Exposition_Apply_pushButton.setObjectName("Exposition_Apply_pushButton")
        self.Exposition_label = QtWidgets.QLabel(self.page_cam)
        self.Exposition_label.setGeometry(QtCore.QRect(0, 82, 101, 51))
        self.Exposition_label.setObjectName("Exposition_label")
        self.Exposition_2_label = QtWidgets.QLabel(self.page_cam)
        self.Exposition_2_label.setGeometry(QtCore.QRect(0, 120, 47, 13))
        self.Exposition_2_label.setObjectName("Exposition_2_label")
        self.toolBox.addItem(self.page_cam, "")

        self.recovery_settings_pushButton = QtWidgets.QPushButton(self.page_base_calibr)
        self.recovery_settings_pushButton.setGeometry(QtCore.QRect(110, 100, 150, 50))
        self.recovery_settings_pushButton.setObjectName("recovery_settings_pushButton")
        self.Calibrate_success_label = QtWidgets.QLabel(self.page_base_calibr)
        self.Calibrate_success_label.setEnabled(False)
        self.Calibrate_success_label.setGeometry(QtCore.QRect(20, 240, 350, 25))
        self.Calibrate_success_label.setScaledContents(False)
        self.Calibrate_success_label.setWordWrap(False)
        self.Calibrate_success_label.setObjectName("Calibrate_success_label")
        self.Control_tabWidget.addTab(self.tab_service, "Сервисные")
        self.verticalLayout.addWidget(self.Control_tabWidget)
        self.tabWidget.addTab(self.Control_page, "")

        self.retranslateUi(Widget)
        self.tabWidget.setCurrentIndex(0)
        self.Control_tabWidget.setCurrentIndex(0)
        self.User_settings_image_toolBox.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(2)
        self.toolBox.layout().setSpacing(6)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.Measure_pushButton.setText(_translate("Widget", "Измерение"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Measure_page), _translate("Widget", "Измерения"))
        self.Mera_number_label.setText(_translate("Widget", "Номер меры"))
        self.Nominal_label.setText(_translate("Widget", "Номинальное"))
        self.Measure_mera_label.setText(_translate("Widget", "Измеренное"))
        self.Mera_number_plus_pushButton.setText(_translate("Widget", "+"))
        self.Nominal_plus_pushButton.setText(_translate("Widget", "+"))
        self.Nominal_minus_pushButton.setText(_translate("Widget", "-"))
        self.Mera_number_minus_pushButton.setText(_translate("Widget", "-"))
        self.Text_calibrate_page_label.setText(_translate("Widget", "Всего мер "))
        self.Mera_num_max_label.setText(_translate("Widget", "0"))
        self.Mera_push_pushButton.setText(_translate("Widget", "Добавить меру"))
        self.Mera_delete_pushButton.setText(_translate("Widget", "Удалить меру"))
        self.Calibrate_start_pushButton.setText(_translate("Widget", "Калибровать"))
        self.Calibrate_save_pushButton.setText(_translate("Widget", "Сохранить калибровку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Calibration_page), _translate("Widget", "Калибровка"))
        self.Capture_image_checkBox.setText(_translate("Widget", "Захват при отсутствии движения"))
        self.EN_Hist_checkBox.setText(_translate("Widget", "Отображать гистограмму"))
        self.Apply_capture_image_pushButton.setText(_translate("Widget", "Применить"))
        self.User_settings_image_toolBox.setItemText(self.User_settings_image_toolBox.indexOf(self.page),
                                                     _translate("Widget", "Параметры захвата изображения"))

        self.White_LED_minus_pushButton.setText(_translate("Widget", "-"))
        self.IR_LED_minus_pushButton.setText(_translate("Widget", "-"))
        self.White_LED_plus_pushButton.setText(_translate("Widget", "+"))
        self.IR_LED_plus_pushButton.setText(_translate("Widget", "+"))
        self.Apply_LED_pushButton.setText(_translate("Widget", "Применить"))
        self.White_LED_label.setText(_translate("Widget", "Белый"))
        self.IR_LED_label.setText(_translate("Widget", "ИК"))
        self.White_LED_lineEdit.setText(_translate("Widget", "0"))
        self.IR_LED_lineEdit.setText(_translate("Widget", "0"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_led), _translate("Widget", "Ток светодиодов"))
        self.Exposition_lineEdit.setText(_translate("Widget", "100"))
        self.Exposition_minus_pushButton.setText(_translate("Widget", "-"))
        self.Exposition_plus_pushButton.setText(_translate("Widget", "+"))
        self.Exposition_Apply_pushButton.setText(_translate("Widget", "Применить"))
        self.Exposition_label.setText(_translate("Widget", "Выдержка"))
        self.Exposition_2_label.setText(_translate("Widget", "мс"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_cam), _translate("Widget", "Параметры камеры"))
        self.recovery_settings_pushButton.setText(_translate("Widget", "Восстановить"))
        self.Calibrate_success_label.setText(_translate("Widget", "Калибровка успешно восстановлена"))
        self.User_settings_image_toolBox.setItemText(self.User_settings_image_toolBox.indexOf(self.page_base_calibr),
                                                     _translate("Widget", "Восстановить заводскую калибровку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Control_page), _translate("Widget", "Настройки"))

        self.setWindowTitle('Контрастометр')
        self.setGeometry(0, 0, 800, 480)