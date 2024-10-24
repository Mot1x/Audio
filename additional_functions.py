import subprocess
from pathlib import Path

exts: list[str] = ['wav', 'mp3']

command_descriptions = {
    'convert': f'Конвертирует аудиофайл в один из доступных форматов ({", ".join(exts)}).',
    'cut': f'Обрезает аудиофайл.',
    'volume': f'Изменяет громкость аудиофайла.',
    'speed': f'Изменяет скорость аудиофайла без изменения тональности.',
    'render': f'Рендерит аудиофайл.',
    'undo': f'Отмена изменений.',
    'redo': f'Возврат отменённых изменений.',
    'quit': f'Выход из утилиты.',
    'help': f'Справка по командам.',
    'splice': f'Склейка текущего и другого файлов',
    'fade_in': f'нарастание звука',
    'fade_out': f'снижение звука',
    'overlay': f'Накладка другого файла',
    'read_file': f'Чтение инструкций из файла',
    'resample_speed': f'Изменяет скорость аудиофайла с изменением тональности.'
}

command_usage = {
    'help': f'help [command], где command - это команда, справка о которой Вас интересует. Если command не задано, '
            f'тогда будет выведена справка обо всех коммандах.',
    'read_file': f'read_file [path], где path - путь к файлу с инструкцией.',
    'render': f'render [path], где path - абсолютный путь к итоговому файлу.',
    'overlay': f'overlay [other_file], где other_file - путь к другому файлу.',
    'splice': f'splice [other_file] [side], где other_file - путь к другому файлу, side - r или l '
              f'(справа или слева присоединение другого файла).',
    'cut': f'cut [start] [stop], где start - начало обрезки, stop - конец обрезки.',
    'fade_in': f'fade_in [start] [time], где start - начало, time - время, за которое звук доберет мощность',
    'fade_out': f'снижение звука, где start - начало, time - время, за которое звук убавит мощность',
    'convert': f'convert [ext], где ext - один из доступных форматов ({", ".join(exts)}).',
    'volume': f'volume [vol], где vol - громкость в процентах (1 = 100%).',
    'speed': f'speed [s], где s - скорость в процентах (1 = 100%).',
    'resample_speed': f'resample_speed [s], где s - скорость в процентах (1 = 100%).',
    'undo': f'undo [count], где count > 0 - количество изменений, которое необходимо отменить.',
    'redo': f'redo [count], где count > 0 - количество изменений, которое необходимо возвратить.',
    'quit': f'quit, и всё)))'
}

command_arguments = {
    'read_file': ['путь'],
    'render': ['путь'],
    'overlay': ['путь'],
    'splice': ['путь', 'сторона'],
    'cut': ['начало', 'конец'],
    'fade_in': ['начало', 'длительность'],
    'fade_out': ['начало', 'длительность'],
    'convert': ['расширение'],
    'volume': ['громкость'],
    'speed': ['скорость'],
    'resample_speed': ['скорость'],
    'undo': ['количество'],
    'redo': ['количество']
}


def get_command_and_args(request: str) -> tuple[str, list[str]]:
    """Деление запроса на команду и аргументы"""
    splited_request: list[str] = request.split('"')

    if len(splited_request) % 2 == 0:
        raise Exception("Проверьте кавычки. Возможно, вы забыли закрыть одну из.")

    command_and_args: list[str] = []
    for index in range(len(splited_request)):
        if index % 2 == 1:
            command_and_args.append(splited_request[index])
            continue
        command_and_args.extend(splited_request[index].split())

    command: str = command_and_args[0]
    args: list[str] = command_and_args[1:]
    return command, args


def print_fail_message(command: str) -> None:
    """Вывод сообщения об ошибке"""
    if command == '':
        print(f'Не было дано команды.')
        return
    print(
        f'Команда не выполнилась. Проверьте существование файла и разрешение '
        f'(подходящие разрешения: {", ".join(exts)}), а также аргументы.\n'
        f'Использование команды: {command_usage[command]}')


def return_fail_message(command: str) -> str:
    """Вывод сообщения об ошибке"""
    if command == '':
        return f'Не было дано команды.'
    return  (f'Команда не выполнилась. '
             f'Проверьте существование файла и разрешение подходящие разрешения: {", ".join(exts)}), '
             f'а также аргументы.')


def run_cmd(command: list[str]) -> int:
    """Запуск процесса с командой"""
    p = subprocess.Popen(command, stderr=subprocess.PIPE)
    p.communicate()
    p.wait()
    return p.returncode


def is_correct_file(file: Path) -> bool:
    """Проверка, что файл существует"""
    if not file.exists():
        print(f"Ошибка: Файл {file} не найден.")
    return file.exists()


def set_output(file: Path, ext=None) -> Path:
    """Составление имени измененного файла"""
    if not ext:
        ext = file.suffix[1:]

    filename: str = file.stem
    path_dir: Path = Path(f'{file.resolve().with_suffix("")}_renders\\')
    path_dir.mkdir(exist_ok=True)
    output: Path = path_dir / f'{filename}.{ext}'

    copy_number: int = 0
    while output.exists():
        copy_number += 1
        output = output.with_stem(f'{filename}_{copy_number}')
    return output


def is_correct_file_and_ext(file: Path, ext=None) -> bool:
    """Проверка на корректоность файла и аудиоформата"""
    if not is_correct_file(file):
        return False
    if ext is None:
        return file.suffix[1:] in exts
    return file.suffix[1:] in exts and ext in exts
