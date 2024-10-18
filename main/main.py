from PyQt5.QtWidgets import QApplication
import sys
from view import CameraApp
from controller import VideoCapture

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    video_cap = VideoCapture(ex)
    ex.show()
    sys.exit(app.exec_())
