import sys
import functions
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Аудиоредактор")
    parser.add_argument("audio", help="Полный путь к аудиофайлу с расширением mp3, wav")
    parser.add_argument('-s', '--simple', action='store_true',
                help="Каждое следующее изменение будет применяться к файлу-источнику, а не к последнему изменению")
    return parser.parse_args()


def get_command_and_args(request):
    command_and_args = request.split(" ")
    command = command_and_args[0]
    args = command_and_args[1:]
    return command, args


def print_fail_message(command):
    print(
        f'Команда не выполнилась. Проверьте существование файла и разрешение '
        f'(подходящие разрешения: {', '.join(functions.FFmpeg.exts)}), а также аргументы.\n'
        f'Использование команды: {functions.FFmpeg.command_usage[command]}')


def main():
    args = parse_args()
    file = functions.FFmpeg(args.audio, args.simple)
    command = ''
    print(f'Ваш файл: {args.audio}\nПростое изменение файла: {args.simple}')

    while True:
        try:
            request = input('> ')
            command, req_args = get_command_and_args(request)

            if command == 'quit':
                sys.exit()

            if command != 'help' and command in file.command_usage.keys():
                local_vars = {'file': file, 'req_args': req_args}
                exec(f'state = file.{command}(*req_args)', globals(), local_vars)
                state = local_vars.get('state')

                if not state:
                    print_fail_message(command)
                else:
                    print(f'Ваш файл: {state}')

            elif command == 'help':
                file.help(*req_args)

            else:
                print(f'Такой команды нет. Существующие команды: {', '.join(file.command_usage.keys())}')

        except Exception as e:
            print(f"Ошибка: {e}")
            print_fail_message(command)


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#    try:
#
#
#        parser = argparse.ArgumentParser(description="Аудиоредактор")
#        subparsers = parser.add_subparsers()
#
#        # Команда load
#        # parser_convert = subparsers.add_parser("load", help="Загружает аудио")
#        # parser_convert.add_argument("path", help="Путь к файлу", type=str)
#        # parser_convert.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio)))
#
#        # Команда convert
#        parser_convert = subparsers.add_parser("convert", help="Преобразовывает формат")
#        parser_convert.add_argument("audio", help="Вставьте аудио")
#        parser_convert.add_argument("ext", help="Формат")
#        parser_convert.add_argument("-b", help="Битрейт звука (по умолчанию 44100)", default=44100, type=int)
#        parser_convert.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).convert_to(args.ext, args.b)))
#
#        # Команда cut
#        parser_cut = subparsers.add_parser("cut", help="Срез")
#        parser_cut.add_argument("audio", help="Вставьте аудио")
#        parser_cut.add_argument('-f', help="Старт")
#        parser_cut.add_argument('-to', help="Стоп")
#        parser_cut.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).cut(args.f, args.to)))
#
#        # Команда volume
#        parser_volume = subparsers.add_parser("volume", help="Изменение громкости")
#        parser_volume.add_argument("audio", help="Вставьте аудио")
#        parser_volume.add_argument("volume", help="Громкость")
#        parser_volume.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).change_volume(args.volume)))
#
#        # Команда speed
#        parser_speed = subparsers.add_parser("speed", help="Изменение скорости")
#        parser_speed.add_argument("audio", help="Вставьте аудио")
#        parser_speed.add_argument("speed", help="Скорость")
#        parser_speed.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).speed_up(args.speed)))
#
#        # Обработка аргументов
#        args = parser.parse_args()
#        args.func(args)
#
#    except Exception as e:
#        print(f"Ошибка : {e}")
