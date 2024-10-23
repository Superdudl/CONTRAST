from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QListWidget
)

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем заголовок окна
        self.setWindowTitle("Настройки приложения")
        self.resize(600, 400)

        # Основной макет
        main_layout = QHBoxLayout()

        # Боковое меню
        menu_list = QListWidget()
        menu_list.addItem("Общие настройки")
        menu_list.addItem("Расширенные настройки")
        menu_list.addItem("Дополнительные параметры")
        menu_list.currentRowChanged.connect(self.display_page)  # связываем выбор с отображением страниц

        # Контентное пространство, где будет меняться содержимое
        self.stack = QStackedWidget()

        # Страница 1: Общие настройки
        general_settings = QWidget()
        general_layout = QVBoxLayout()
        general_layout.addWidget(QLabel("Здесь общие настройки"))
        general_layout.addWidget(QPushButton("Опция 1"))
        general_layout.addWidget(QPushButton("Опция 2"))
        general_settings.setLayout(general_layout)

        # Страница 2: Расширенные настройки
        advanced_settings = QWidget()
        advanced_layout = QVBoxLayout()
        advanced_layout.addWidget(QLabel("Здесь расширенные настройки"))
        advanced_layout.addWidget(QPushButton("Опция 3"))
        advanced_layout.addWidget(QPushButton("Опция 4"))
        advanced_settings.setLayout(advanced_layout)

        # Страница 3: Дополнительные параметры
        extra_settings = QWidget()
        extra_layout = QVBoxLayout()
        extra_layout.addWidget(QLabel("Здесь дополнительные параметры"))
        extra_layout.addWidget(QPushButton("Опция 5"))
        extra_layout.addWidget(QPushButton("Опция 6"))
        extra_settings.setLayout(extra_layout)

        # Добавляем страницы в QStackedWidget
        self.stack.addWidget(general_settings)
        self.stack.addWidget(advanced_settings)
        self.stack.addWidget(extra_settings)

        # Добавляем меню и контентное пространство в основной макет
        main_layout.addWidget(menu_list)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def display_page(self, index):
        # Отображаем выбранную страницу
        self.stack.setCurrentIndex(index)

# Запуск приложения
if __name__ == '__main__':
    app = QApplication([])
    window = SettingsWindow()
    window.show()
    app.exec_()