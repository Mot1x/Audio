import argparse
from functools import partial
import additional_functions
import functions

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget


def parse_args_from_string(args_str: str) -> argparse.Namespace:
    """Парсит аргументы из строки"""
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                        help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    parser.add_argument('-r', '--read', type=str, help="Прочитать инструкции из файла")

    # Преобразуем строку в список аргументов
    args_list = args_str.split()

    # Парсим аргументы из списка
    args, unknown = parser.parse_known_args(args_list)

    return args


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file = None
        self.setWindowTitle("Аудиоредактор")
        self.setFixedSize(QSize(800, 750))

        self.label1 = QLabel(self)
        self.label1.setText("Введите путь к аудио")
        self.label1.setGeometry(310, 50, 200, 30)

        self.input = QLineEdit(self)
        self.input.setGeometry(290, 100, 200, 30)
        self.button = QPushButton("Ввод завершен", self)
        self.button.setGeometry(290, 150, 200, 30)
        self.button.clicked.connect(lambda: self.the_button_was_clicked(self.input.text()))

        self.message_label = QLabel(self)
        self.message_label.setGeometry(20, 200, 760, 40)

        self.buttons = []
        self.buttons_inputs = []

        self.edit_font()
        self.add_button_functions()

    def edit_font(self):
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.message_label.setFont(font)
        self.input.setFont(font)

    def the_button_was_clicked(self, input_data):
        try:
            parsed_args = parse_args_from_string(input_data)
            self.file = functions.FFmpeg(parsed_args.audio, parsed_args.simple)
            print(f'Ваш файл: {parsed_args.audio}\nПростое изменение файла: {parsed_args.simple}')
            self.message_label.setText(f'Ваш файл: {parsed_args.audio} Простое изменение файла: {parsed_args.simple}')
        except SystemExit:
            print("Ошибка: неверные аргументы")

    def add_button_functions(self):
        y = 250
        k = 70
        for func in additional_functions.command_usage.keys():
            # функции одного короткого аргумента
            if func in ['convert', 'volume', 'speed', 'resample_speed']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(300, y, 40, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons_inputs.append(input_button)
                y += 40
            # функции одного длинного аргумента
            elif func in ['render', 'help', 'overlay', 'read_file']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(300, y, 370, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons_inputs.append(input_button)
                y += 40
            # функции двух аргументов
            elif func in ['cut', 'splice']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button1 = QLineEdit(self)
                input_button1.setGeometry(300, y, 170, 30)
                self.buttons_inputs.append(input_button1)
                input_button2 = QLineEdit(self)
                input_button2.setGeometry(500, y, 170, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button1, input_button2))
                self.buttons_inputs.append(input_button2)
                y += 40
            # функция без аргументов
            elif func in ['fade_in', 'fade_out']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(300, y, 0, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons_inputs.append(input_button)
                y += 40
            # функции одного короткого аргумента, расположенные сверху
            elif func in ['undo', 'redo']:
                button = QPushButton(func, self)
                button.setGeometry(640, k, 60, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(700, k, 60, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons_inputs.append(input_button)
                k += 40
            self.buttons.append(button)

    def execute_command(self, command, input_button1, input_button2=None):
        if self.file:
            args = [input_button1.text()]
            if input_button2:
                args.append(input_button2.text())
            result = self.file.execute_in_window(command, *args)
            self.message_label.setText(result)
