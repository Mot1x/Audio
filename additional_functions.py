import subprocess
import os
from pathlib import Path

exts = ['wav', 'mp3']

command_descriptions = {
    'convert': f'Конвертирует аудиофайл в один из доступных форматов ({", ".join(exts)}).',
    'cut': f'Обрезает аудиофайл.',
    'volume': f'Изменяет громкость аудиофайла.',
    'speed': f'Изменяет скорость аудиофайла.',
    'render': f'Рендерит аудиофайл.',
    'undo': f'Отмена изменений.',
    'redo': f'Возврат отменённых изменений.',
    'quit': f'Выход из утилиты.',
    'help': f'Справка по командам.',
    'splice': f'Склейка текущего и другого файлов',
    'overlay': f'Накладка другого файла',
    'read_file': f'Чтение инструкций из файла',
    'resample_speed': f'Второй способ ускорения.'
}

command_usage = {
    'convert': f'convert [ext], где ext - один из доступных форматов ({", ".join(exts)}).',
    'cut': f'cut [start] [stop], где start - начало обрезки, stop - конец обрезки.',
    'volume': f'volume [vol], где vol - громкость в процентах (1 = 100%).',
    'speed': f'speed [s], где s - скорость в процентах (1 = 100%).',
    'render': f'render [path], где path - абсолютный путь к итоговому файлу.',
    'undo': f'undo [count], где count > 0 - количество изменений, которое необходимо отменить.',
    'redo': f'redo [count], где count > 0 - количество изменений, которое необходимо возвратить.',
    'quit': f'quit, и всё)))',
    'help': f'help [command], где command - это команда, справка о которой Вас интересует. Если command не задано, '
            f'тогда будет выведена справка обо всех коммандах.',
    'splice': f'splice [other_file] [side], где other_file - путь к другому файлу, side - r или l'
              f'(справа или слева присоединение другого файла).',
    'overlay': f'overlay [other_file], где other_file - путь к другому файлу.',
    'read_file': f'read_file [path], где path - путь к файлу с инструкцией.',
    'resample_speed': f'resample_speed [s], где s - скорость в процентах (1 = 100%).'
}


def get_command_and_args(request):
    """Деление запроса на команду и аргументы"""
    command_and_args = request.split(" ")
    command = command_and_args[0]
    args = command_and_args[1:]
    return command, args


def print_fail_message(command):
    """Вывод сообщения об ошибке"""
    if command == '':
        print(f'Не было дано команды.')
        return

    print(
        f'Команда не выполнилась. Проверьте существование файла и разрешение '
        f'(подходящие разрешения: {", ".join(exts)}), а также аргументы.\n'
        f'Использование команды: {command_usage[command]}')


def run_cmd(command):
    """Запуск процесса с командой"""
    p = subprocess.Popen(command, stderr=subprocess.PIPE)
    p.communicate()
    p.wait()
    return p.returncode


def is_correct_file(file):
    """Проверка, что файл существует"""
    if not os.path.exists(file):
        print(f"Ошибка: Файл {file} не найден.")
    return os.path.exists(file)


def set_output(file, ext=None):
    """Составление имени измененного файла"""
    if not ext:
        ext = file[-3:]
    path_dir = f'{file[:-4]} renders\\'
    os.makedirs(path_dir, exist_ok=True)
    name = file.split("\\")[-1][:-4]
    new_name = name
    copy_number = 0
    while Path(f'{path_dir}{new_name}.{ext}').exists():
        copy_number += 1
        new_name = f'{name} ({copy_number})'
    return f'{path_dir}{new_name}.{ext}'


def is_correct_file_and_ext(file, ext=None):
    """Проверка на корректоность файла и аудиоформата"""
    if not is_correct_file(file):
        return False
    if ext is None:
        return file[-3:] in exts
    return file[-3:] in exts and ext in exts
