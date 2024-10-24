from functools import partial
import additional_functions

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QApplication

import functions


class SecondWindow(QMainWindow):
    def __init__(self, file: functions.FFmpeg, name_file: str):
        super().__init__()
        self._file = file
        self.setWindowTitle("Редактирование аудио")
        self.setFixedSize(QSize(800, 600))

        self._buttons = []
        self._buttons_inputs = []
        self._add_button_functions()

        self._lable_current_file = QLabel(self)
        self._lable_current_file.setGeometry(500, 20, 300, 30)
        self._lable_current_file.setText(f'Ваш файл: {name_file}')

        self._message_label = QLabel(self)
        self._message_label.setGeometry(20, 40, 740, 70)
        self._edit_font()

    def _edit_font(self) -> None:
        """Настройка шрифта"""
        font = QFont()
        font.setPointSize(12)
        self._lable_current_file.setFont(font)
        self._message_label.setFont(font)
        self._message_label.setFont(font)

    def _add_button_functions(self) -> None:
        """Добавлени в окно всех кнопок-функций"""
        y = 140
        k = 500
        for func in additional_functions.command_usage.keys():
            if func not in ['quit', 'help', 'undo', 'redo']:
                self._add_button_help(func, y)

            if func in ['convert', 'volume', 'speed', 'resample_speed']:
                self._add_button_for_short_arg_function(func, y)

            elif func in ['render', 'overlay', 'read_file']:
                self._add_button_for_long_arg_function(func, y)

            elif func in ['splice']:
                self._add_button_for_two_long_arg_func(func, y)

            elif func in ['cut', 'fade_in', 'fade_out']:
                self._add_button_for_two_short_arg_func(func, y)

            elif func in ['undo', 'redo']:
                self._add_button_redo_or_undo(k, func)
                k += 40
            if func not in ['quit', 'help', 'undo', 'redo']:
                y += 40

    def _execute_command(self, command: str, input_button1: QLineEdit, input_button2: QLineEdit = None) -> None:
        """Выполнение команды при нажатии кнопки"""
        args = [input_button1.text()]
        if input_button2:
            args.append(input_button2.text())
        result = self._file.execute_in_window(command, *args)
        self._message_label.setText(result)

    def _add_button_help(self, func: str, y: int) -> None:
        """Создание кнопки help для конкретной команды"""
        button_help = QPushButton("?", self)
        button_help.setGeometry(20, y, 20, 30)
        button_help.clicked.connect(partial(self._button_help_was_clicked, func))
        self._buttons.append(button_help)

    def _button_help_was_clicked(self, command: str) -> None:
        """Вывод help для конкретной команды"""
        result = self._file.execute_in_window("help", command)
        self._message_label.setText(result)

    def _add_button_redo_or_undo(self, k: int, func: str) -> None:
        """Кнопки для функций в правом нижнем углу"""
        button = QPushButton(func, self)
        button.setGeometry(640, k, 60, 30)
        input_button = QLineEdit(self)
        input_button.setGeometry(700, k, 60, 30)
        button.clicked.connect(partial(self._execute_command, func, input_button))
        self._buttons_inputs.append(input_button)
        self._buttons.append(button)
        button_help = QPushButton("?", self)
        button_help.setGeometry(610, k, 20, 30)
        button_help.clicked.connect(partial(self._button_help_was_clicked, func))
        self._buttons.append(button_help)

    def _add_button_for_short_arg_function(self, func: str, y: int) -> None:
        """Кнопки для функций одного короткого аргумента"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)
        input_button = QLineEdit(self)
        input_button.setGeometry(300, y, 40, 30)
        button.clicked.connect(partial(self._execute_command, func, input_button))
        self._buttons.append(button)
        self._buttons_inputs.append(input_button)

    def _add_button_for_long_arg_function(self, func: str, y: int) -> None:
        """Кнопки для функций одного длинного аргумента"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)
        input_button = QLineEdit(self)
        input_button.setGeometry(300, y, 370, 30)
        button.clicked.connect(partial(self._execute_command, func, input_button))
        self._buttons.append(button)
        self._buttons_inputs.append(input_button)

    def _add_button_for_two_short_arg_func(self, func: str, y: int) -> None:
        """Кнопки для функций двух коротких аргументов"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)
        input_button1 = QLineEdit(self)
        input_button1.setGeometry(300, y, 40, 30)
        self._buttons_inputs.append(input_button1)
        self._buttons.append(button)
        input_button2 = QLineEdit(self)
        input_button2.setGeometry(360, y, 40, 30)
        button.clicked.connect(partial(self._execute_command, func, input_button1, input_button2))
        self._buttons_inputs.append(input_button2)

    def _add_button_for_two_long_arg_func(self, func: str, y: int) -> None:
        """Кнопки для функций двух длинных аргументов"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)
        input_button1 = QLineEdit(self)
        input_button1.setGeometry(300, y, 170, 30)
        self._buttons_inputs.append(input_button1)
        self._buttons.append(button)
        input_button2 = QLineEdit(self)
        input_button2.setGeometry(500, y, 170, 30)
        button.clicked.connect(partial(self._execute_command, func, input_button1, input_button2))
        self._buttons_inputs.append(input_button2)
