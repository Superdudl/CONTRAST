# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form4.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView

from view import resources
from utils import MlpCanvas


class CameraApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 480)
        Widget.setMaximumSize(QtCore.QSize(800, 480))
        Widget.setMinimumSize(QtCore.QSize(800, 480))
        Widget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Img_label = QtWidgets.QLabel(Widget)
        self.Img_label.setGeometry(QtCore.QRect(2, 0, 360, 480))
        self.Img_label.setMaximumSize(QtCore.QSize(480, 720))
        self.Img_label.setFrameShape(QtWidgets.QFrame.Box)
        self.Img_label.setText("")
        self.Img_label.setObjectName("Img_label")
        self.tabWidget = QtWidgets.QTabWidget(Widget)
        self.tabWidget.setGeometry(QtCore.QRect(364, 0, 439, 483))
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
        self.Contrast_Label = QtWidgets.QLabel(self.Measure_page)
        self.Contrast_Label.setGeometry(QtCore.QRect(164, 240, 131, 81))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.Contrast_Label.setFont(font)
        self.Contrast_Label.setText("0.00")
        self.Contrast_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Contrast_Label.setObjectName("Contrast_Label")
        self.Measure_pushButton = QtWidgets.QPushButton(self.Measure_page)
        self.Measure_pushButton.setEnabled(True)
        self.Measure_pushButton.setGeometry(QtCore.QRect(32, 362, 371, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Measure_pushButton.setFont(font)
        self.Measure_pushButton.setIconSize(QtCore.QSize(21, 16))
        self.Measure_pushButton.setObjectName("Measure_pushButton")
        self.Hist_Widget = QtWidgets.QWidget(self.Measure_page)
        self.Hist_Widget.setGeometry(QtCore.QRect(6, 6, 421, 249))
        self.Hist_Widget.setObjectName("Hist_Widget")
        self.Hist_Label = QtWidgets.QLabel(self.Hist_Widget)
        self.Hist_Label.setGeometry(QtCore.QRect(16, 6, 384, 192))
        self.Hist_Label.setMinimumSize(QtCore.QSize(384, 192))
        self.Hist_Label.setMaximumSize(QtCore.QSize(512, 256))
        self.Hist_Label.setFrameShape(QtWidgets.QFrame.Box)
        self.Hist_Label.setText("")
        self.Hist_Label.setScaledContents(False)
        self.Hist_Label.setObjectName("Hist_Label")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.Hist_Widget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 200, 416, 24))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.hist_ticks = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.hist_ticks.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.hist_ticks.setContentsMargins(0, 0, 0, 0)
        self.hist_ticks.setHorizontalSpacing(66)
        self.hist_ticks.setObjectName("hist_ticks")
        self.hist_tick_50 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.hist_tick_50.setMinimumSize(QtCore.QSize(30, 0))
        self.hist_tick_50.setMaximumSize(QtCore.QSize(30, 16777215))
        self.hist_tick_50.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hist_tick_50.setAlignment(QtCore.Qt.AlignCenter)
        self.hist_tick_50.setObjectName("hist_tick_50")
        self.hist_ticks.addWidget(self.hist_tick_50, 0, 2, 1, 1)
        self.hist_tick_0 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.hist_tick_0.setMinimumSize(QtCore.QSize(30, 0))
        self.hist_tick_0.setMaximumSize(QtCore.QSize(30, 16777215))
        self.hist_tick_0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hist_tick_0.setAlignment(QtCore.Qt.AlignCenter)
        self.hist_tick_0.setObjectName("hist_tick_0")
        self.hist_ticks.addWidget(self.hist_tick_0, 0, 0, 1, 1)
        self.hist_tick_75 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.hist_tick_75.setMinimumSize(QtCore.QSize(30, 0))
        self.hist_tick_75.setMaximumSize(QtCore.QSize(30, 16777215))
        self.hist_tick_75.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hist_tick_75.setAlignment(QtCore.Qt.AlignCenter)
        self.hist_tick_75.setObjectName("hist_tick_75")
        self.hist_ticks.addWidget(self.hist_tick_75, 0, 3, 1, 1)
        self.hist_tick_100 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.hist_tick_100.setMinimumSize(QtCore.QSize(30, 0))
        self.hist_tick_100.setMaximumSize(QtCore.QSize(30, 16777215))
        self.hist_tick_100.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hist_tick_100.setAlignment(QtCore.Qt.AlignCenter)
        self.hist_tick_100.setObjectName("hist_tick_100")
        self.hist_ticks.addWidget(self.hist_tick_100, 0, 4, 1, 1)
        self.hist_tick_25 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.hist_tick_25.setMinimumSize(QtCore.QSize(30, 0))
        self.hist_tick_25.setMaximumSize(QtCore.QSize(30, 16777215))
        self.hist_tick_25.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hist_tick_25.setAlignment(QtCore.Qt.AlignCenter)
        self.hist_tick_25.setObjectName("hist_tick_25")
        self.hist_ticks.addWidget(self.hist_tick_25, 0, 1, 1, 1)
        self.tabWidget.addTab(self.Measure_page, "")
        self.Calibration_page = QtWidgets.QWidget()
        self.Calibration_page.setObjectName("Calibration_page")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.Calibration_page)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 6, 435, 443))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.Calib_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.Calib_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Calib_verticalLayout.setObjectName("Calib_verticalLayout")
        self.Calib_tab = QtWidgets.QTabWidget(self.verticalLayoutWidget_2)
        self.Calib_tab.setObjectName("Calib_tab")
        self.Calib_basic = QtWidgets.QWidget()
        self.Calib_basic.setObjectName("Calib_basic")
        self.Mera_num_max_label = QtWidgets.QLabel(self.Calib_basic)
        self.Mera_num_max_label.setGeometry(QtCore.QRect(266, 8, 50, 50))
        self.Mera_num_max_label.setText("")
        self.Mera_num_max_label.setObjectName("Mera_num_max_label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.Calib_basic)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(16, 270, 391, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.Calib_buttons_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.Calib_buttons_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.Calib_buttons_gridLayout.setObjectName("Calib_buttons_gridLayout")
        self.Mera_push_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mera_push_pushButton.sizePolicy().hasHeightForWidth())
        self.Mera_push_pushButton.setSizePolicy(sizePolicy)
        self.Mera_push_pushButton.setObjectName("Mera_push_pushButton")
        self.Calib_buttons_gridLayout.addWidget(self.Mera_push_pushButton, 2, 0, 1, 1)
        self.Mera_delete_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mera_delete_pushButton.sizePolicy().hasHeightForWidth())
        self.Mera_delete_pushButton.setSizePolicy(sizePolicy)
        self.Mera_delete_pushButton.setObjectName("Mera_delete_pushButton")
        self.Calib_buttons_gridLayout.addWidget(self.Mera_delete_pushButton, 2, 2, 1, 1)
        self.Calibrate_start_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_start_pushButton.sizePolicy().hasHeightForWidth())
        self.Calibrate_start_pushButton.setSizePolicy(sizePolicy)
        self.Calibrate_start_pushButton.setObjectName("Calibrate_start_pushButton")
        self.Calib_buttons_gridLayout.addWidget(self.Calibrate_start_pushButton, 3, 0, 1, 1)
        self.Calibrate_save_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_save_pushButton.sizePolicy().hasHeightForWidth())
        self.Calibrate_save_pushButton.setSizePolicy(sizePolicy)
        self.Calibrate_save_pushButton.setObjectName("Calibrate_save_pushButton")
        self.Calib_buttons_gridLayout.addWidget(self.Calibrate_save_pushButton, 3, 2, 1, 1)
        self.Text_calibrate_page_label = QtWidgets.QLabel(self.Calib_basic)
        self.Text_calibrate_page_label.setGeometry(QtCore.QRect(14, 8, 300, 50))
        self.Text_calibrate_page_label.setObjectName("Text_calibrate_page_label")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.Calib_basic)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(-4, 62, 436, 196))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_calib_panel = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_calib_panel.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_calib_panel.setObjectName("gridLayout_calib_panel")
        self.Mera_number_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Mera_number_label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Mera_number_label.setObjectName("Mera_number_label")
        self.gridLayout_calib_panel.addWidget(self.Mera_number_label, 4, 0, 1, 1)
        self.Nominal_minus_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.Nominal_minus_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.Nominal_minus_pushButton.setMaximumSize(QtCore.QSize(50, 50))
        self.Nominal_minus_pushButton.setObjectName("Nominal_minus_pushButton")
        self.gridLayout_calib_panel.addWidget(self.Nominal_minus_pushButton, 0, 1, 1, 1)
        self.Measure_mera_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Measure_mera_label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Measure_mera_label.setObjectName("Measure_mera_label")
        self.gridLayout_calib_panel.addWidget(self.Measure_mera_label, 2, 0, 1, 1)
        self.Nominal_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Nominal_lineEdit.setMinimumSize(QtCore.QSize(100, 45))
        self.Nominal_lineEdit.setMaximumSize(QtCore.QSize(100, 45))
        self.Nominal_lineEdit.setMaxLength(4)
        self.Nominal_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Nominal_lineEdit.setReadOnly(False)
        self.Nominal_lineEdit.setObjectName("Nominal_lineEdit")
        self.gridLayout_calib_panel.addWidget(self.Nominal_lineEdit, 0, 2, 1, 1)
        self.Nominal_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Nominal_label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Nominal_label.setObjectName("Nominal_label")
        self.gridLayout_calib_panel.addWidget(self.Nominal_label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_calib_panel.addItem(spacerItem, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_calib_panel.addItem(spacerItem1, 1, 0, 1, 1)
        self.Mera_number_plus_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.Mera_number_plus_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.Mera_number_plus_pushButton.setMaximumSize(QtCore.QSize(50, 50))
        self.Mera_number_plus_pushButton.setObjectName("Mera_number_plus_pushButton")
        self.gridLayout_calib_panel.addWidget(self.Mera_number_plus_pushButton, 4, 3, 1, 1)
        self.Measure_mera_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Measure_mera_lineEdit.setMinimumSize(QtCore.QSize(100, 45))
        self.Measure_mera_lineEdit.setMaximumSize(QtCore.QSize(100, 45))
        self.Measure_mera_lineEdit.setText("")
        self.Measure_mera_lineEdit.setMaxLength(3)
        self.Measure_mera_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Measure_mera_lineEdit.setReadOnly(True)
        self.Measure_mera_lineEdit.setObjectName("Measure_mera_lineEdit")
        self.gridLayout_calib_panel.addWidget(self.Measure_mera_lineEdit, 2, 2, 1, 1)
        self.Mera_number_minus_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.Mera_number_minus_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.Mera_number_minus_pushButton.setMaximumSize(QtCore.QSize(50, 50))
        self.Mera_number_minus_pushButton.setObjectName("Mera_number_minus_pushButton")
        self.gridLayout_calib_panel.addWidget(self.Mera_number_minus_pushButton, 4, 1, 1, 1)
        self.Mera_number_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Mera_number_lineEdit.setMinimumSize(QtCore.QSize(100, 45))
        self.Mera_number_lineEdit.setMaximumSize(QtCore.QSize(100, 45))
        self.Mera_number_lineEdit.setMaxLength(3)
        self.Mera_number_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Mera_number_lineEdit.setReadOnly(True)
        self.Mera_number_lineEdit.setObjectName("Mera_number_lineEdit")
        self.gridLayout_calib_panel.addWidget(self.Mera_number_lineEdit, 4, 2, 1, 1)
        self.Nominal_plus_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.Nominal_plus_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.Nominal_plus_pushButton.setMaximumSize(QtCore.QSize(50, 50))
        self.Nominal_plus_pushButton.setObjectName("Nominal_plus_pushButton")
        self.gridLayout_calib_panel.addWidget(self.Nominal_plus_pushButton, 0, 3, 1, 1)
        self.Refresh_ADC_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.Refresh_ADC_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.Refresh_ADC_pushButton.setMaximumSize(QtCore.QSize(50, 50))
        self.Refresh_ADC_pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Refresh_ADC_pushButton.setIcon(icon)
        self.Refresh_ADC_pushButton.setIconSize(QtCore.QSize(32, 32))
        self.Refresh_ADC_pushButton.setObjectName("Refresh_ADC_pushButton")
        self.gridLayout_calib_panel.addWidget(self.Refresh_ADC_pushButton, 2, 3, 1, 1)
        self.Calib_tab.addTab(self.Calib_basic, "")
        self.Calib_additional = QtWidgets.QWidget()
        self.Calib_additional.setObjectName("Calib_additional")
        self.Mera_Table = QtWidgets.QTableWidget(self.Calib_additional)
        self.Mera_Table.setGeometry(QtCore.QRect(2, 6, 425, 127))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mera_Table.sizePolicy().hasHeightForWidth())
        self.Mera_Table.setSizePolicy(sizePolicy)
        self.Mera_Table.setObjectName("Mera_Table")
        self.Mera_Table.setColumnCount(4)
        self.Mera_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Mera_Table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Mera_Table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Mera_Table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Mera_Table.setHorizontalHeaderItem(3, item)
        self.Mera_Table.verticalHeader().setVisible(False)
        self.Mera_Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.Calib_additional)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(3, 141, 423, 263))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.Mera_Plot = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.Mera_Plot.setContentsMargins(0, 0, 0, 50)
        self.Mera_Plot.setObjectName("Mera_Plot")
        self.canvas = MlpCanvas(self, width=5, height=4, dpi=100)
        self.Mera_Plot.addWidget(self.canvas)

        self.Calib_tab.addTab(self.Calib_additional, "")
        self.Calib_verticalLayout.addWidget(self.Calib_tab)
        self.tabWidget.addTab(self.Calibration_page, "")
        self.Control_page = QtWidgets.QWidget()
        self.Control_page.setObjectName("Control_page")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Control_page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 9, 435, 439))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Control_tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.Control_tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control_tabWidget.sizePolicy().hasHeightForWidth())
        self.Control_tabWidget.setSizePolicy(sizePolicy)
        self.Control_tabWidget.setMouseTracking(False)
        self.Control_tabWidget.setToolTipDuration(-1)
        self.Control_tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.Control_tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.Control_tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.Control_tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.Control_tabWidget.setUsesScrollButtons(False)
        self.Control_tabWidget.setTabBarAutoHide(True)
        self.Control_tabWidget.setObjectName("Control_tabWidget")
        self.User_tab = QtWidgets.QWidget()
        self.User_tab.setObjectName("User_tab")
        self.listWidget = QtWidgets.QListWidget(self.User_tab)
        self.listWidget.setGeometry(QtCore.QRect(2, 0, 427, 161))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.stackedWidget = QtWidgets.QStackedWidget(self.User_tab)
        self.stackedWidget.setGeometry(QtCore.QRect(6, 170, 417, 211))
        self.stackedWidget.setTabletTracking(False)
        self.stackedWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stackedWidget.setAutoFillBackground(True)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.stackedWidget.addWidget(self.page_5)
        self.page_img_cap = QtWidgets.QWidget()
        self.page_img_cap.setTabletTracking(False)
        self.page_img_cap.setObjectName("page_img_cap")
        self.Capture_image_checkBox = QtWidgets.QCheckBox(self.page_img_cap)
        self.Capture_image_checkBox.setGeometry(QtCore.QRect(30, 20, 310, 50))
        self.Capture_image_checkBox.setObjectName("Capture_image_checkBox")
        self.EN_Hist_checkBox = QtWidgets.QCheckBox(self.page_img_cap)
        self.EN_Hist_checkBox.setGeometry(QtCore.QRect(30, 68, 310, 50))
        self.EN_Hist_checkBox.setObjectName("EN_Hist_checkBox")
        self.Apply_capture_image_pushButton = QtWidgets.QPushButton(self.page_img_cap)
        self.Apply_capture_image_pushButton.setGeometry(QtCore.QRect(122, 150, 180, 50))
        self.Apply_capture_image_pushButton.setObjectName("Apply_capture_image_pushButton")
        self.stackedWidget.addWidget(self.page_img_cap)
        self.page_recover = QtWidgets.QWidget()
        self.page_recover.setObjectName("page_recover")
        self.recovery_settings_pushButton_2 = QtWidgets.QPushButton(self.page_recover)
        self.recovery_settings_pushButton_2.setGeometry(QtCore.QRect(140, 74, 150, 50))
        self.recovery_settings_pushButton_2.setObjectName("recovery_settings_pushButton_2")
        self.stackedWidget.addWidget(self.page_recover)

        self.calib_page = QtWidgets.QWidget()
        self.calib_page.setObjectName("calib_page")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.calib_page)
        self.calib_units = QtWidgets.QCheckBox(self.calib_page)
        self.calib_units.setGeometry(QtCore.QRect(30, 68, 330, 40))
        self.stackedWidget.addWidget(self.calib_page)

        self.page_about_sys = QtWidgets.QWidget()
        self.page_about_sys.setObjectName("page_about_sys")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.page_about_sys)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(14, 34, 389, 151))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_about_sys)
        self.Control_tabWidget.addTab(self.User_tab, "Пользовательские")
        self.tab_service = QtWidgets.QWidget()
        self.tab_service.setObjectName("tab_service")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_service)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 0, 429, 151))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setStyleSheet("")
        self.listWidget_2.setObjectName("listWidget_2")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.tab_service)
        self.stackedWidget_2.setGeometry(QtCore.QRect(6, 160, 417, 221))
        self.stackedWidget_2.setTabletTracking(False)
        self.stackedWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stackedWidget_2.setAutoFillBackground(True)
        self.stackedWidget_2.setStyleSheet("")
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.stackedWidget_2.addWidget(self.page_6)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setTabletTracking(False)
        self.page_3.setObjectName("page_3")
        self.White_LED_label = QtWidgets.QLabel(self.page_3)
        self.White_LED_label.setGeometry(QtCore.QRect(20, 10, 60, 50))
        self.White_LED_label.setObjectName("White_LED_label")
        self.IR_LED_label = QtWidgets.QLabel(self.page_3)
        self.IR_LED_label.setGeometry(QtCore.QRect(20, 70, 60, 50))
        self.IR_LED_label.setObjectName("IR_LED_label")
        self.White_LED_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.White_LED_lineEdit.setGeometry(QtCore.QRect(184, 6, 70, 50))
        self.White_LED_lineEdit.setMaxLength(3)
        self.White_LED_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.White_LED_lineEdit.setReadOnly(True)
        self.White_LED_lineEdit.setObjectName("White_LED_lineEdit")
        self.IR_LED_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.IR_LED_lineEdit.setGeometry(QtCore.QRect(184, 64, 70, 50))
        self.IR_LED_lineEdit.setMaxLength(3)
        self.IR_LED_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.IR_LED_lineEdit.setReadOnly(True)
        self.IR_LED_lineEdit.setObjectName("IR_LED_lineEdit")
        self.White_LED_plus_pushButton = QtWidgets.QPushButton(self.page_3)
        self.White_LED_plus_pushButton.setGeometry(QtCore.QRect(266, 6, 50, 50))
        self.White_LED_plus_pushButton.setObjectName("White_LED_plus_pushButton")
        self.White_LED_minus_pushButton = QtWidgets.QPushButton(self.page_3)
        self.White_LED_minus_pushButton.setGeometry(QtCore.QRect(122, 6, 50, 50))
        self.White_LED_minus_pushButton.setObjectName("White_LED_minus_pushButton")
        self.IR_LED_plus_pushButton = QtWidgets.QPushButton(self.page_3)
        self.IR_LED_plus_pushButton.setGeometry(QtCore.QRect(264, 64, 50, 50))
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.IR_LED_plus_pushButton.setFont(font)
        self.IR_LED_plus_pushButton.setObjectName("IR_LED_plus_pushButton")
        self.IR_LED_minus_pushButton = QtWidgets.QPushButton(self.page_3)
        self.IR_LED_minus_pushButton.setGeometry(QtCore.QRect(122, 64, 50, 50))
        self.IR_LED_minus_pushButton.setObjectName("IR_LED_minus_pushButton")
        self.White_LED_Switch = QtWidgets.QPushButton(self.page_3)
        self.White_LED_Switch.setGeometry(QtCore.QRect(338, 6, 50, 50))
        self.White_LED_Switch.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/switch.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.White_LED_Switch.setIcon(icon1)
        self.White_LED_Switch.setIconSize(QtCore.QSize(20, 20))
        self.White_LED_Switch.setCheckable(True)
        self.White_LED_Switch.setChecked(True)
        self.White_LED_Switch.setObjectName("White_LED_Switch")
        self.IR_LED_Switch = QtWidgets.QPushButton(self.page_3)
        self.IR_LED_Switch.setGeometry(QtCore.QRect(338, 64, 50, 50))
        self.IR_LED_Switch.setText("")
        self.IR_LED_Switch.setIcon(icon1)
        self.IR_LED_Switch.setIconSize(QtCore.QSize(20, 20))
        self.IR_LED_Switch.setCheckable(True)
        self.IR_LED_Switch.setChecked(True)
        self.IR_LED_Switch.setObjectName("IR_LED_Switch")
        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.Exposition_label = QtWidgets.QLabel(self.page_4)
        self.Exposition_label.setGeometry(QtCore.QRect(20, 30, 101, 51))
        self.Exposition_label.setObjectName("Exposition_label")
        self.Exposition_2_label = QtWidgets.QLabel(self.page_4)
        self.Exposition_2_label.setGeometry(QtCore.QRect(20, 70, 47, 13))
        self.Exposition_2_label.setObjectName("Exposition_2_label")
        self.Exposition_minus_pushButton = QtWidgets.QPushButton(self.page_4)
        self.Exposition_minus_pushButton.setGeometry(QtCore.QRect(140, 40, 50, 50))
        self.Exposition_minus_pushButton.setObjectName("Exposition_minus_pushButton")
        self.Exposition_lineEdit = QtWidgets.QLineEdit(self.page_4)
        self.Exposition_lineEdit.setGeometry(QtCore.QRect(200, 40, 70, 50))
        self.Exposition_lineEdit.setMaxLength(5)
        self.Exposition_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Exposition_lineEdit.setObjectName("Exposition_lineEdit")
        self.Exposition_plus_pushButton = QtWidgets.QPushButton(self.page_4)
        self.Exposition_plus_pushButton.setGeometry(QtCore.QRect(280, 40, 50, 50))
        self.Exposition_plus_pushButton.setObjectName("Exposition_plus_pushButton")
        self.Exposition_Apply_pushButton = QtWidgets.QPushButton(self.page_4)
        self.Exposition_Apply_pushButton.setGeometry(QtCore.QRect(140, 120, 191, 50))
        self.Exposition_Apply_pushButton.setObjectName("Exposition_Apply_pushButton")
        self.stackedWidget_2.addWidget(self.page_4)
        self.Control_tabWidget.addTab(self.tab_service, "Сервисные")
        self.verticalLayout.addWidget(self.Control_tabWidget)
        self.tabWidget.addTab(self.Control_page, "")

        self.retranslateUi(Widget)
        self.tabWidget.setCurrentIndex(0)
        self.Calib_tab.setCurrentIndex(0)
        self.Control_tabWidget.setCurrentIndex(0)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.Measure_pushButton.setText(_translate("Widget", "Измерение"))
        self.hist_tick_50.setText(_translate("Widget", "50"))
        self.hist_tick_0.setText(_translate("Widget", "0"))
        self.hist_tick_75.setText(_translate("Widget", "75"))
        self.hist_tick_100.setText(_translate("Widget", "100"))
        self.hist_tick_25.setText(_translate("Widget", "25"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Measure_page), _translate("Widget", "Измерения"))
        self.Mera_push_pushButton.setText(_translate("Widget", "Добавить меру"))
        self.Mera_delete_pushButton.setText(_translate("Widget", "Удалить меру"))
        self.Calibrate_start_pushButton.setText(_translate("Widget", "Калибровать"))
        self.Calibrate_save_pushButton.setText(_translate("Widget", "Сохранить калибровку"))
        self.Text_calibrate_page_label.setText(_translate("Widget", "Всего калибровочных мер"))
        self.Mera_number_label.setText(_translate("Widget", "Номер меры"))
        self.Nominal_minus_pushButton.setText(_translate("Widget", "-"))
        self.Measure_mera_label.setText(_translate("Widget", "Измеренное"))
        self.Nominal_label.setText(_translate("Widget", "Номинальное"))
        self.Mera_number_plus_pushButton.setText(_translate("Widget", "+"))
        self.Mera_number_minus_pushButton.setText(_translate("Widget", "-"))
        self.Nominal_plus_pushButton.setText(_translate("Widget", "+"))
        self.Calib_tab.setTabText(self.Calib_tab.indexOf(self.Calib_basic), _translate("Widget", "Основные"))
        item = self.Mera_Table.horizontalHeaderItem(0)
        item.setText(_translate("Widget", "ID"))
        item = self.Mera_Table.horizontalHeaderItem(1)
        item.setText(_translate("Widget", "АЦП"))
        item = self.Mera_Table.horizontalHeaderItem(2)
        item.setText(_translate("Widget", "Номинал"))
        item = self.Mera_Table.horizontalHeaderItem(3)
        item.setText(_translate("Widget", "Результат"))
        self.Calib_tab.setTabText(self.Calib_tab.indexOf(self.Calib_additional), _translate("Widget", "Дополнительные"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Calibration_page), _translate("Widget", "Калибровка"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Widget", "Параметры захвата изображения"))
        item = self.listWidget.item(1)
        item.setText(_translate("Widget", "Восстановить заводскую калибровку"))
        item = self.listWidget.item(2)
        item.setText(_translate("Widget", "Калибровка"))
        item = self.listWidget.item(3)
        item.setText(_translate("Widget", "О системе"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.Capture_image_checkBox.setText(_translate("Widget", "Захват при отсутствии движения"))
        self.EN_Hist_checkBox.setText(_translate("Widget", "Отображать гистограмму"))
        self.calib_units.setText(_translate("Widget", "В единицах оптической плотности"))
        self.Apply_capture_image_pushButton.setText(_translate("Widget", "Применить"))
        self.recovery_settings_pushButton_2.setText(_translate("Widget", "Восстановить"))
        self.label_2.setText(_translate("Widget", "0.1"))
        self.label.setText(_translate("Widget", "Версия:"))
        self.label_6.setText(_translate("Widget", "192.168.0.1"))
        self.label_3.setText(_translate("Widget", "Дата:"))
        self.label_5.setText(_translate("Widget", "IP"))
        self.label_4.setText(_translate("Widget", "30.10.2024"))
        self.label_7.setText(_translate("Widget", "Port"))
        self.label_8.setText(_translate("Widget", "55555"))
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        item = self.listWidget_2.item(0)
        item.setText(_translate("Widget", "Ток светодиодов"))
        item = self.listWidget_2.item(1)
        item.setText(_translate("Widget", "Параметры камеры"))
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.White_LED_label.setText(_translate("Widget", "Белый"))
        self.IR_LED_label.setText(_translate("Widget", "ИК"))
        self.White_LED_lineEdit.setText(_translate("Widget", "0"))
        self.IR_LED_lineEdit.setText(_translate("Widget", "0"))
        self.White_LED_plus_pushButton.setText(_translate("Widget", "+"))
        self.White_LED_minus_pushButton.setText(_translate("Widget", "-"))
        self.IR_LED_plus_pushButton.setText(_translate("Widget", "+"))
        self.IR_LED_minus_pushButton.setText(_translate("Widget", "-"))
        self.Exposition_label.setText(_translate("Widget", "Выдержка"))
        self.Exposition_2_label.setText(_translate("Widget", "мс"))
        self.Exposition_minus_pushButton.setText(_translate("Widget", "-"))
        self.Exposition_lineEdit.setText(_translate("Widget", "100"))
        self.Exposition_plus_pushButton.setText(_translate("Widget", "+"))
        self.Exposition_Apply_pushButton.setText(_translate("Widget", "Применить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Control_page), _translate("Widget", "Настройки"))
