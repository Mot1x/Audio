import argparse
from pathlib import Path

import additional_functions
import functions
import secondWindow

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog


def parse_args_from_string(args_str: str) -> argparse.Namespace:
    """Парсит аргументы из строки"""
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                        help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    parser.add_argument('-r', '--read', type=str, help="Прочитать инструкции из файла")
    args_list = args_str
    args, unknown = parser.parse_known_args(args_list)
    return args


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._file = None
        self.setWindowTitle("Аудиоредактор")
        self.setFixedSize(QSize(400, 250))

        self._label_input = QLabel(self)
        self._label_input.setText("Введите путь к аудио")
        self._label_input.setGeometry(120, 50, 155, 30)

        self._line_input = QLineEdit(self)
        self._line_input.setGeometry(100, 100, 160, 30)
        self._line_input.setPlaceholderText("Выберите файл")
        self._line_input.setReadOnly(True)

        self._open_file_button = QPushButton(self)
        self._open_file_button.setIcon(QIcon("img/folder.png"))
        self._open_file_button.setIconSize(QSize(20, 20))
        self._open_file_button.setGeometry(270, 100, 30, 30)
        self._open_file_button.clicked.connect(lambda: self._open_file_button_was_clicked())

        self._button = QPushButton("Начать редактировать", self)
        self._button.setGeometry(100, 150, 200, 30)
        self._button.clicked.connect(lambda: self._the_button_was_clicked(self._line_input.text()))

        self._message_label = QLabel(self)
        self._message_label.setGeometry(20, 200, 760, 40)

        self.new_window = None
        self._edit_font()

    def _edit_font(self) -> None:
        """Настройка шрифта"""
        font = QFont()
        font.setPointSize(12)
        self._label_input.setFont(font)
        self._message_label.setFont(font)
        self._line_input.setFont(font)

    def _the_button_was_clicked(self, file_path: str) -> None:
        """Обработчик кнопки"""
        try:
            self._file = functions.FFmpeg(file_path, False)
            if not additional_functions.is_correct_file(Path(file_path)):
                self._message_label.setText(f'Файл не существует')
                return

            self._message_label.setText(f'Ваш файл: {file_path}')
            self.new_window = secondWindow.SecondWindow(self._file, file_path)
            self.new_window.show()
            self.window().close()
        except SystemExit:
            print("Ошибка: неверные аргументы")

    def _open_file_button_was_clicked(self) -> None:
        """Обработчик кнопки открытия файла"""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Выбрать файл", "", "Audio Files (*.wav *.mp3)")
        if file_path:
            self._line_input.setText(file_path)
