from PyQt5.QtWidgets import QApplication
import sys
import platform
from pathlib import Path, PurePath
from view import CameraApp
from controller import MainController

sys.path.append(str(PurePath(Path(__file__).parent.parent)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path(PurePath(Path(__file__).parent.parent, 'view', 'styleSheet.qss')).read_text())
    ex = CameraApp()
    main_controller = MainController(ex)
    if platform.system() != "Windows":
        ex.showFullScreen()
    else:
        ex.show()
    sys.exit(app.exec_())
