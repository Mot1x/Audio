from functools import partial
import additional_functions

from PyQt6.QtCore import QSize, QTimer, QRegularExpression
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QApplication, QSpinBox, QDateTimeEdit, \
    QFileDialog, QTextEdit, QComboBox

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

        self._label_current_file = QLineEdit(self)
        self._label_current_file.setGeometry(20, 20, 760, 35)
        self._label_current_file.setText(f'Стартовый файл: {name_file}')
        self._label_current_file.setReadOnly(True)

        self._message_label = QTextEdit(self)
        self._message_label.setGeometry(20, 65, 760, 65)
        self._message_label.setReadOnly(True)
        self._edit_font()

    def _edit_font(self) -> None:
        """Настройка шрифта"""
        font = QFont()
        font.setPointSize(12)
        self._label_current_file.setFont(font)
        self._message_label.setFont(font)
        self._message_label.setFont(font)

    def _add_button_functions(self) -> None:
        """Добавление в окно всех кнопок-функций"""
        y = 140
        k = 500
        for func in additional_functions.command_usage.keys():
            if func not in ['quit', 'help', 'undo', 'redo']:
                self._add_button_help(func, y)

            if func in ['volume', 'speed', 'resample_speed']:
                self._add_button_for_short_arg_function(func, y)

            elif func in ['convert']:
                self._add_button_for_choise_arg_function(func, y)

            elif func in ['render', 'overlay']:
                self._add_button_for_pathfile_arg_function(func, y, 'mp3/wav')

            elif func in ['read_file']:
                self._add_button_for_pathfile_arg_function(func, y, 'txt')

            elif func in ['splice']:
                self._add_button_for_two_long_arg_func(func, y)

            elif func in ['cut', 'fade_in', 'fade_out']:
                self._add_button_for_two_short_arg_func(func, y)

            elif func in ['undo', 'redo']:
                self._add_button_redo_or_undo(k, func)
                k += 40
            if func not in ['quit', 'help', 'undo', 'redo']:
                y += 40

    def _execute_command(self, command: str, button: QPushButton,
                         input_button1: QLineEdit | QDateTimeEdit | QSpinBox | QComboBox,
                         input_button2: QLineEdit | QDateTimeEdit | QComboBox = None) -> None:
        """Выполнение команды при нажатии кнопки"""
        self._highlight_button(button)
        args = []
        if isinstance(input_button1, QLineEdit):
            args.append(input_button1.text())
        elif isinstance(input_button1, QDateTimeEdit):
            total_seconds_input1 = input_button1.time().msecsSinceStartOfDay() / 1000.0
            args.append(str(total_seconds_input1))
        elif isinstance(input_button1, QSpinBox):
            args.append(input_button1.text())
        elif isinstance(input_button1, QComboBox):
            args.append(input_button1.currentText())

        if isinstance(input_button2, QLineEdit):
            args.append(input_button2.text())
        elif isinstance(input_button2, QDateTimeEdit):
            total_seconds_input2 = input_button2.time().msecsSinceStartOfDay() / 1000.0
            args.append(str(total_seconds_input2))
        elif isinstance(input_button2, QComboBox):
            args.append(input_button2.currentText())

        result = self._file.execute_in_window(command, *args)
        self._message_label.setText(result)

    def _highlight_button(self, button: QPushButton) -> None:
        """Изменение цвета кнопки на 3 секунды"""
        original_style = button.styleSheet()
        button.setStyleSheet("background-color: green;")
        QTimer.singleShot(1000, lambda: button.setStyleSheet(original_style))

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

    def _open_file_button_was_clicked(self, ext: str, input_button) -> None:
        """Обработчик кнопки открытия файла"""
        file_dialog = QFileDialog(self)
        ext_filter = "Audio Files (*.wav *.mp3)"

        if ext == 'txt':
            ext_filter = "Text Files (*.txt)"

        file_path, _ = file_dialog.getOpenFileName(self, "Выбрать файл", "", ext_filter)
        if file_path:
            input_button.setText(file_path)

    def _save_file_button_was_clicked(self, input_button) -> None:
        """Обработчик кнопки открытия файла"""
        file_dialog = QFileDialog(self)
        ext_filter = "Audio Files (*.wav *.mp3)"

        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить файл", "", ext_filter)
        if file_path:
            input_button.setText(file_path)

    def _add_button_redo_or_undo(self, k: int, func: str) -> None:
        """Кнопки для функций в правом нижнем углу"""
        button = QPushButton(func, self)
        button.setGeometry(600, k, 60, 30)
        input_button = QSpinBox(self)
        input_button.setGeometry(670, k, 100, 30)
        input_button.setMinimum(1)

        button.clicked.connect(partial(self._execute_command, func, button, input_button))
        self._buttons_inputs.append(input_button)
        self._buttons.append(button)

        button_help = QPushButton("?", self)
        button_help.setGeometry(570, k, 20, 30)
        button_help.clicked.connect(partial(self._button_help_was_clicked, func))

        self._buttons.append(button_help)

    def _add_button_for_short_arg_function(self, func: str, y: int) -> None:
        """Кнопки для функций одного короткого аргумента"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)

        input_button = QLineEdit(self)
        input_button.setGeometry(300, y, 100, 30)
        input_button.setPlaceholderText(additional_functions.command_arguments[func][0])

        regexp = QRegularExpression(r"^(\d+(\.\d*)?|\.\d+)?$")
        validator = QRegularExpressionValidator(regexp, input_button)
        input_button.setValidator(validator)

        button.clicked.connect(partial(self._execute_command, func, button, input_button))
        self._buttons.append(button)
        self._buttons_inputs.append(input_button)

    def _add_button_for_pathfile_arg_function(self, func: str, y: int, ext: str) -> None:
        """Кнопки для функций одного длинного аргумента"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)

        input_button = QLineEdit(self)
        input_button.setGeometry(300, y, 330, 30)
        input_button.setPlaceholderText(additional_functions.command_arguments[func][0])
        input_button.setReadOnly(True)

        self._open_file_button = QPushButton(self)
        self._open_file_button.setIcon(QIcon("img/folder.png"))
        self._open_file_button.setIconSize(QSize(20, 20))
        self._open_file_button.setGeometry(640, y, 30, 30)

        if func == 'render':
            self._open_file_button.clicked.connect(lambda: self._save_file_button_was_clicked(input_button))
        else:
            self._open_file_button.clicked.connect(lambda: self._open_file_button_was_clicked(ext, input_button))

        button.clicked.connect(partial(self._execute_command, func, button, input_button))
        self._buttons.append(button)
        self._buttons_inputs.append(input_button)

    def _add_button_for_two_short_arg_func(self, func: str, y: int) -> None:
        """Кнопки для функций двух коротких аргументов"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)

        input_button1 = QDateTimeEdit(self)
        input_button1.setDisplayFormat("mm:ss.zzz")
        input_button1.setGeometry(300, y, 100, 30)
        self._buttons_inputs.append(input_button1)

        input_button2 = QDateTimeEdit(self)
        input_button2.setDisplayFormat("mm:ss.zzz")
        input_button2.setGeometry(420, y, 100, 30)
        self._buttons_inputs.append(input_button2)

        self._buttons.append(button)
        button.clicked.connect(partial(self._execute_command, func, button, input_button1, input_button2))

    def _add_button_for_two_long_arg_func(self, func: str, y: int) -> None:
        """Кнопки для функций двух длинных аргументов"""
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)

        input_button1 = QLineEdit(self)
        input_button1.setGeometry(300, y, 330, 30)
        input_button1.setPlaceholderText(additional_functions.command_arguments[func][0])
        self._buttons_inputs.append(input_button1)
        input_button1.setReadOnly(True)

        self._open_file_button = QPushButton(self)
        self._open_file_button.setIcon(QIcon("img/folder.png"))
        self._open_file_button.setIconSize(QSize(20, 20))
        self._open_file_button.setGeometry(640, y, 30, 30)

        self._buttons.append(button)

        input_button2 = QComboBox(self)
        input_button2.setGeometry(680, y, 100, 30)
        input_button2.setPlaceholderText(additional_functions.command_arguments[func][1])
        input_button2.addItems(['l', 'r'])

        self._open_file_button.clicked.connect(lambda: self._open_file_button_was_clicked('mp3/wav', input_button1))
        button.clicked.connect(partial(self._execute_command, func, button, input_button1, input_button2))
        self._buttons_inputs.append(input_button2)

    def _add_button_for_choise_arg_function(self, func, y):
        button = QPushButton(func, self)
        button.setGeometry(50, y, 200, 30)

        combo_box = QComboBox(self)
        combo_box.setGeometry(300, y, 100, 30)
        combo_box.setPlaceholderText(additional_functions.command_arguments[func][0])
        combo_box.addItems(["mp3", "wav"])

        button.clicked.connect(partial(self._execute_command, func, button, combo_box))
        self._buttons.append(button)
        self._buttons_inputs.append(combo_box)
