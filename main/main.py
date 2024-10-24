from PyQt5.QtWidgets import QApplication
import sys
from pathlib import Path, PurePath

sys.path.append(str(PurePath(Path(__file__).parent.parent)))
from view import CameraApp2
from controller import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path(PurePath(Path(__file__).parent.parent, 'view', 'styleSheet.qss')).read_text())
    ex = CameraApp2()
    main_controller = MainController(ex)
    ex.show()
    sys.exit(app.exec_())
