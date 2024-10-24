import argparse
from functools import partial
from pathlib import Path

import additional_functions
import functions
import secondWindow

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit


def parse_args_from_string(args_str: str) -> argparse.Namespace:
    """Парсит аргументы из строки"""
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                        help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    parser.add_argument('-r', '--read', type=str, help="Прочитать инструкции из файла")
    args_list = args_str.split()
    args, unknown = parser.parse_known_args(args_list)
    return args


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._file = None
        self.setWindowTitle("Аудиоредактор")
        self.setFixedSize(QSize(800, 300))

        self._label_input = QLabel(self)
        self._label_input.setText("Введите путь к аудио")
        self._label_input.setGeometry(310, 50, 200, 30)

        self._line_input = QLineEdit(self)
        self._line_input .setGeometry(290, 100, 200, 30)
        self._button = QPushButton("Ввод завершен", self)
        self._button.setGeometry(290, 150, 200, 30)
        self._button.clicked.connect(lambda: self._the_button_was_clicked(self._line_input .text()))

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
        self._line_input .setFont(font)

    def _the_button_was_clicked(self, input_data: str) -> None:
        """Обработчик кнопки"""
        try:
            parsed_args = parse_args_from_string(input_data)
            self._file = functions.FFmpeg(parsed_args.audio, parsed_args.simple)
            if not additional_functions.is_correct_file(Path(parsed_args.audio)):
                self._message_label.setText(f'Файл не существует')
            else:
                self._message_label.setText(f'Ваш файл: {parsed_args.audio}')

                self.new_window = secondWindow.SecondWindow(self._file, parsed_args.audio)
                self.new_window.show()

        except SystemExit:
            print("Ошибка: неверные аргументы")


