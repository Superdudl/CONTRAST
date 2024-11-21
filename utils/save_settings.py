from PyQt5.QtCore import QSettings
from PyQt5 import QtCore
from pathlib import Path, PurePath

def save_settings(view):
    path = Path(PurePath(Path(__file__).parent.parent, 'src', 'settings.ini'))
    settings = QSettings(str(path), QSettings.Format.IniFormat)

    # Параметры захвата изображения
    settings.setValue('img_capture_params/EN_Hist_checkBox', view.EN_Hist_checkBox.isChecked())
    settings.setValue('img_capture_params/Capture_image_checkBox', view.Capture_image_checkBox.isChecked())
    settings.setValue('img_capture_params/Contrast_Label', view.Contrast_Label.saveGeometry())
    settings.setValue('img_capture_params/Contrast_Font', view.Contrast_Label.font().pointSize())

    # Единицы измерения
    settings.setValue('units/units', view.units.isChecked())
    settings.setValue('units/units2', view.units2.isChecked())
    settings.setValue('units/units3', view.units3.isChecked())

    # Выдержка
    settings.setValue('timeExposure', float(view.Exposition_lineEdit.text().replace(',', '.')) * 1000)

    # ШИМ
    settings.setValue('whitePWM', float(view.White_LED_lineEdit.text()))
    settings.setValue('irPWM', float(view.IR_LED_lineEdit.text()))



