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
        f'(подходящие разрешения: {", ".join(functions.FFmpeg.exts)}), а также аргументы.\n'
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

            if command == 'read_file':
                file.read_file(req_args)

            elif command != 'help' and command in file.command_usage.keys():
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
                print(f'Такой команды нет. Существующие команды: {", ".join(file.command_usage.keys())}')

        except Exception as e:
            print(f"Ошибка: {e}")
            print_fail_message(command)


if __name__ == "__main__":
    main()
