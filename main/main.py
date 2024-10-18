from PyQt5.QtWidgets import QApplication
import sys
from view import CameraApp
from controller import MainController, VideoCapture

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    main_controller = MainController(ex)
    ex.show()
    sys.exit(app.exec_())
