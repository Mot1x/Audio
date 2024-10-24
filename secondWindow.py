from functools import partial
import additional_functions

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QApplication


class SecondWindow(QMainWindow):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.setWindowTitle("Аудиоредактор и изменения")
        self.setFixedSize(QSize(800, 600))

        self.buttons = []
        self.buttons_inputs = []
        self.add_button_functions()

        self.message_label = QLabel(self)
        self.message_label.setGeometry(60, 20, 740, 70)
        self.message_label.setText("Строка состояния")

    def add_button_functions(self):
        y = 80
        k = 500
        for func in additional_functions.command_usage.keys():
            # функции одного короткого аргумента
            if func in ['convert', 'volume', 'speed', 'resample_speed']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(300, y, 40, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons.append(button)
                self.buttons_inputs.append(input_button)
                button_help = QPushButton("?", self)
                button_help.setGeometry(20, y, 20, 30)
                button_help.clicked.connect(partial(self.button_help_was_clicked, func))
                self.buttons.append(button_help)
                y += 40
            # функции одного длинного аргумента
            elif func in ['render', 'overlay', 'read_file']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(300, y, 370, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons.append(button)
                self.buttons_inputs.append(input_button)
                button_help = QPushButton("?", self)
                button_help.setGeometry(20, y, 20, 30)
                button_help.clicked.connect(partial(self.button_help_was_clicked, func))
                self.buttons.append(button_help)
                y += 40
            # функции двух аргументов
            elif func in ['splice']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button1 = QLineEdit(self)
                input_button1.setGeometry(300, y, 170, 30)
                self.buttons_inputs.append(input_button1)
                self.buttons.append(button)
                input_button2 = QLineEdit(self)
                input_button2.setGeometry(500, y, 170, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button1, input_button2))
                self.buttons_inputs.append(input_button2)
                button_help = QPushButton("?", self)
                button_help.setGeometry(20, y, 20, 30)
                button_help.clicked.connect(partial(self.button_help_was_clicked, func))
                self.buttons.append(button_help)
                y += 40
            # функции двух коротких аргументов
            elif func in ['cut', 'fade_in', 'fade_out']:
                button = QPushButton(func, self)
                button.setGeometry(50, y, 200, 30)
                input_button1 = QLineEdit(self)
                input_button1.setGeometry(300, y, 40, 30)
                self.buttons_inputs.append(input_button1)
                self.buttons.append(button)
                input_button2 = QLineEdit(self)
                input_button2.setGeometry(360, y, 40, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button1, input_button2))
                self.buttons_inputs.append(input_button2)
                button_help = QPushButton("?", self)
                button_help.setGeometry(20, y, 20, 30)
                button_help.clicked.connect(partial(self.button_help_was_clicked, func))
                self.buttons.append(button_help)
                y += 40
            # функции одного короткого аргумента, расположенные сверху
            elif func in ['undo', 'redo']:
                button = QPushButton(func, self)
                button.setGeometry(640, k, 60, 30)
                input_button = QLineEdit(self)
                input_button.setGeometry(700, k, 60, 30)
                button.clicked.connect(partial(self.execute_command, func, input_button))
                self.buttons_inputs.append(input_button)
                self.buttons.append(button)
                button_help = QPushButton("?", self)
                button_help.setGeometry(20, k, 20, 30)
                button_help.clicked.connect(partial(self.button_help_was_clicked, func))
                self.buttons.append(button_help)
                k += 40

    def execute_command(self, command, input_button1, input_button2=None):
        if self.file:
            args = [input_button1.text()]
            if input_button2:
                args.append(input_button2.text())
            result = self.file.execute_in_window(command, *args)
            self.message_label.setText(result)

    def button_help_was_clicked(self, command):
        if self.file:
            result = self.file.execute_in_window("help", command)
            self.message_label.setText(result)
