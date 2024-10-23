from PyQt5.QtWidgets import QApplication
import sys
from pathlib import Path
sys.path.append("..")
from view import CameraApp2
from controller import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('../view/styleSheet.qss').read_text())
    ex = CameraApp2()
    main_controller = MainController(ex)
    ex.show()
    sys.exit(app.exec_())
