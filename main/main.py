from PyQt5.QtWidgets import QApplication
import sys
import platform
from pathlib import Path, PurePath

sys.path.append(str(PurePath(Path(__file__).parent.parent)))
from view import CameraApp
from controller import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    style_path = PurePath(Path(__file__).parent.parent, 'src', 'styleSheet.qss')
    app.setStyleSheet(Path(style_path).read_text())
    ex = CameraApp()
    main_controller = MainController(ex)
    if platform.system() != "Windows":
        ex.showFullScreen()
    else:
        ex.show()
    sys.exit(app.exec_())
