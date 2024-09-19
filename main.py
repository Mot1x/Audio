import sys
from functions import FFmpeg
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    parser.add_argument('-r', '--read', type=str, help="Прочитать инструкции из файла")
    return parser.parse_args()


def main():
    args = parse_args()
    file = FFmpeg(args.audio, args.simple)
    command = ''
    print(f'Ваш файл: {args.audio}\nПростое изменение файла: {args.simple}')

    while True:
        try:
            request = input('> ') if not args.read else f'read_file {args.read}'
            command, req_args = FFmpeg.get_command_and_args(request)
            file.execute(command, req_args)
            if args.read:
                break

        except Exception as e:
            print(f"Ошибка: {e}")
            FFmpeg.print_fail_message(command)


if __name__ == "__main__":
    main()
