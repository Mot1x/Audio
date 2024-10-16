import sys
from PyQt6.QtWidgets import QApplication

from functions import FFmpeg
import argparse
import additional_functions
import mainWindow


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    parser.add_argument('-r', '--read', type=str, help="Прочитать инструкции из файла")
    return parser.parse_args()


def main() -> None:
    args: argparse.Namespace = parse_args()
    file: FFmpeg = FFmpeg(args.audio, args.simple)
    command: str = ''
    print(f'Ваш файл: {args.audio}\nПростое изменение файла: {args.simple}')

    while True:
        try:
            request: str = input('> ') if not args.read else f'read_file {args.read}'
            command: str = additional_functions.get_command_and_args(request)[0]
            req_args: list[str] = additional_functions.get_command_and_args(request)[1]
            file.execute(command, req_args)
            if args.read:
                break

        except Exception as e:
            print(f"Ошибка: {e}")
            additional_functions.print_fail_message(command)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow()
    window.show()
    app.exec()
