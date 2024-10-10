import argparse
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
        self.setFixedSize(QSize(800, 600))

        self.label1 = QLabel(self)
        self.label1.setText("Введите путь к аудио")
        self.label1.setGeometry(310, 50, 200, 30)

        self.input = QLineEdit(self)
        self.input.setGeometry(290, 100, 200, 30)

        self.button = QPushButton("Ввод завершен", self)
        self.button.setGeometry(290, 150, 200, 30)
        self.button.clicked.connect(lambda: self.the_button_was_clicked(self.input.text()))

        self.label2 = QLabel(self)
        self.label2.setGeometry(20, 200, 760, 40)

        self.button_convert = QPushButton("convert", self)
        self.input_convert = QLineEdit(self)
        self.button_cut = QPushButton("cut", self)
        self.input_cut = QLineEdit(self)
        self.button_volume = QPushButton("volume", self)
        self.input_volume = QLineEdit(self)
        self.button_splice = QPushButton("splice", self)
        self.input_splice = QLineEdit(self)
        self.button_overlay = QPushButton("overlay", self)
        self.input_overlay = QLineEdit(self)
        self.button_speed = QPushButton("speed", self)
        self.input_speed = QLineEdit(self)
        self.button_resample_speed = QPushButton("resample_speed", self)
        self.input_resample_speed = QLineEdit(self)
        self.button_read_file = QPushButton("read_file", self)
        self.input_read_file = QLineEdit(self)
        self.button_render = QPushButton("render", self)
        self.input_render = QLineEdit(self)

        self.edit_font()
        self.add_buttom_functions()

    def edit_font(self):
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label2.setFont(font)
        self.input.setFont(font)

    def the_button_was_clicked(self, input_data):
        try:
            parsed_args = parse_args_from_string(input_data)
            self.file = functions.FFmpeg(parsed_args.audio, parsed_args.simple)
            print(f'Ваш файл: {parsed_args.audio}\nПростое изменение файла: {parsed_args.simple}')
            self.label2.setText(f'Ваш файл: {parsed_args.audio} Простое изменение файла: {parsed_args.simple}')
        except SystemExit:
            print("Ошибка: неверные аргументы")

    def add_buttom_functions(self):
        self.button_convert.setGeometry(50, 250, 200, 30)
        self.input_convert.setGeometry(300, 250, 400, 30)
        self.button_convert.clicked.connect(lambda: self.file.functions.FFmpeg.execute("convert", self.input_convert.text()))

        self.button_cut.setGeometry(50, 290, 200, 30)
        self.input_cut.setGeometry(300, 290, 400, 30)
        self.button_cut.clicked.connect(lambda: self.file.functions.FFmpeg.execute("cut", self.input_cut.text()))

        self.button_volume.setGeometry(50, 330, 200, 30)
        self.input_volume.setGeometry(290, 330, 200, 30)
        self.button_volume.clicked.connect(lambda: self.file.functions.FFmpeg.execute("volume", self.input_volume.text()))

        self.button_splice.setGeometry(50, 370, 200, 30)
        self.input_splice.setGeometry(300, 370, 400, 30)
        self.button_splice.clicked.connect(lambda: self.file.functions.FFmpeg.execute("splice", self.input_splice.text()))

        self.button_overlay.setGeometry(50, 410, 200, 30)
        self.input_overlay.setGeometry(300, 410, 400, 30)
        self.button_overlay.clicked.connect(lambda: self.file.functions.FFmpeg.execute("overlay", self.input_overlay.text()))

        self.button_speed.setGeometry(50, 450, 200, 30)
        self.input_speed.setGeometry(300, 450, 400, 30)
        self.button_speed.clicked.connect(lambda: self.file.functions.FFmpeg.execute("speed", self.input_speed.text()))

        self.button_resample_speed.setGeometry(50, 490, 200, 30)
        self.input_resample_speed.setGeometry(300, 490, 400, 30)
        self.button_resample_speed.clicked.connect(lambda: self.file.functions.FFmpeg.execute("resample_speed", self.input_resample_speed.text()))

        self.button_read_file.setGeometry(50, 530, 200, 30)
        self.input_read_file.setGeometry(300, 530, 400, 30)
        self.button_read_file.clicked.connect(lambda: self.file.functions.FFmpeg.execute("read_file", self.input_read_file.text()))



