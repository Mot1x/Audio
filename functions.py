import os
import subprocess
import main
import re


class FFmpeg:
    cmds = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    cmds_probe = 'C:\\ffmpeg\\bin\\ffprobe.exe'
    exts = ['wav', 'mp3']

    command_descriptions = {
        'convert': f'Конвертирует аудиофайл в один из доступных форматов ({", ".join(exts)}).',
        'cut': f'Обрезает аудиофайл.',
        'volume': f'Изменяет громкость аудиофайла.',
        'speed': f'Изменяет скорость аудиофайла.',
        'render': f'Рендерит аудиофайл.',
        'undo': f'Отмена изменений.',
        'quit': f'Выход из утилиты.',
        'help': f'Справка по командам.',
        'splice': f'Склейка текущего и другого файлов',
        'overlay': f'Накладка другого файла',
        #'read_file': f'Чтение инструкций из файла',
        'speed2': f'торой способ ускорения'
    }

    command_usage = {
        'convert': f'convert [ext], где ext - один из доступных форматов ({", ".join(exts)}).',
        'cut': f'cut [start] [stop], где start - начало обрезки, stop - конец обрезки.',
        'volume': f'volume [vol], где vol - громкость в процентах (1 = 100%).',
        'speed': f'speed [s], где s - скорость в процентах (1 = 100%).',
        'render': f'render [path], где path - абсолютный путь к итоговому файлу.',
        'undo': f'undo [count], где count > 0 - количество изменений, которое необходимо отменить.',
        'quit': f'quit, и всё)))',
        'help': f'help [command], где command - это команда, справка о которой Вас интересует. Если command не задано, '
                f'тогда будет выведена справка обо всех коммандах',
        'splice': f'splice [other_file] [side], где other_file - путь к другому файлу, side - r или l'
                  f'(справа или слева присоединение другого файла)',
        'overlay': f'overlay [other_file], где other_file - путь к другому файлу',
        #'read_file': f'read_file [уть к файлу с инструкцией]',
        'speed2': f'speed2 [скорость]'
    }

    def __init__(self, file, is_simple):
        self.file = file
        self.current_path = file
        self.history = [self.file]
        self.edit_count = 0
        self.is_simple = is_simple

    def is_correct_file(self):
        if not os.path.exists(self.file):
            print(f"Ошибка: Файл {self.file} не найден.")
        return os.path.exists(self.file)

    def run_cmd(self, command):
        p = subprocess.Popen(command, stderr=subprocess.PIPE)
        p.communicate()
        p.wait()
        return p.returncode

    def add_to_history(self, output):
        if not self.is_simple:
            self.edit_count += 1
            self.current_path = output
            self.history.append(self.current_path)

    def set_output(self, ext=None):
        if not ext:
            ext = self.file[-3:]

        path_dir = f'{self.file[:-4]} renders\\'
        os.makedirs(path_dir, exist_ok=True)
        name = self.file.split("\\")[-1][:-4]
        new_name = name

        i = 0
        while os.path.exists(f'{path_dir}{new_name}.{ext}'):
            i += 1
            new_name = f'{name} ({i})'

        return f'{path_dir}{new_name}.{ext}'

    #def set_output(self, ext=None):
    #    path = os.path.dirname(os.path.abspath(__file__))
    #    name = self.file.split("\\")[-1][:-4]
    #    if len(name) >= 4:
    #        ending_name = name[-4:]
    #        match = re.search(r" \(\d\)$", ending_name)
    #        if bool(match):
    #            self.edit_count = int(name[-2]) + 1
    #            name = name[:-4]
    #        else:
    #            os.makedirs(path + "\\" + name, exist_ok=True)
    #    folder = name + "\\"
    #    return path + "\\" + folder + f'{name}.{ext}' if ext \
    #        else (path + "\\" + folder + f'{name} ({self.edit_count}){self.file[-4:]}')

    def convert(self, ext=None, bitrate=44100):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and ext in FFmpeg.exts:
            output = self.set_output(ext)
            command = [FFmpeg.cmds, '-i', self.current_path, '-ac', '2', '-ar', str(bitrate), '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def cut(self, start=None, stop=None):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()

            command = [FFmpeg.cmds, '-i', self.current_path]
            if start:
                command.extend(['-ss', start])
            if stop:
                command.extend(['-to', stop])
            command.extend(['-y', output])

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def volume(self, volume=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds, '-i', self.current_path, '-af', f'volume={volume}', '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def splice(self, other_file, side="r"):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and FFmpeg(other_file).is_correct_file():
            output = self.set_output()
            command = []
            if side == "r":
                command = [
                    'ffmpeg',
                    '-i', os.path.abspath(self.current_path),
                    '-i', other_file,
                    '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[out]',
                    '-map', '[out]',
                    '-c:a', 'copy',
                    output
                ]
            if side == "l":
                command = [
                    'ffmpeg',
                    '-i', other_file,
                    '-i', os.path.abspath(self.current_path),
                    '-c', 'copy',
                    '-map', '0',
                    '-map', '1',
                    '-metadata:s:a:0', 'title="Первый файл"',
                    '-metadata:s:a:1', 'title="Второй файл"',
                    '-metadata', 'title="Объединенный файл"',
                    output
                ]
            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def overlay(self, other_file):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and FFmpeg(other_file).is_correct_file():
            output = self.set_output()
            command = [
                'ffmpeg',
                '-i', os.path.abspath(self.current_path),
                '-i', other_file,
                '-filter_complex', '[0:a][1:a]amix=inputs=2',
                output
            ]
            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def speed(self, speed=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds, '-i', os.path.abspath(self.current_path), '-af', f'rubberband=tempo={speed}', '-y',
                       output]
            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def read_file(self, input_file):
        with open(input_file) as file_program:
            commands = file_program.readlines()
            for command in commands:
                if not command.isspace():
                    command = command.strip()
                    command, req_args = main.get_command_and_args(command)
                    if command != 'help' and command != 'quit' and command in FFmpeg.command_usage.keys():
                        local_vars = {'file': self, 'req_args': req_args}
                        exec(f'state = file.{command}(*req_args)', globals(), local_vars)
                        state = local_vars.get('state')

                        if not state:
                            main.print_fail_message(command)
                        else:
                            print(f'Ваш файл: {state}')

    def speed2(self, speed=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds, '-i', os.path.abspath(self.current_path), '-af', f'atempo={speed}', '-y',
                       output]
            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            else:
                return False
        else:
            return False

    def render(self, path=None):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and path:
            command = [FFmpeg.cmds, '-i', self.current_path, '-y', path]
            self.run_cmd(command)
            return path
        else:
            return False

    def help(self, command=None):
        if not command:
            for command in self.command_descriptions.keys():
                print(f'{command} - {self.command_descriptions[command]}\nИспользование: {self.command_usage[command]}\n')

        elif command in self.command_descriptions.keys():
            print(f'{command} - {self.command_descriptions[command]}\nИспользование: {self.command_usage[command]}')

        else:
            print(f'Такой команды нет. Существующие команды: {", ".join(self.command_usage.keys())}')

        return True

    def undo(self, count=1):
        count = int(count)
        if self.is_simple:
            raise Exception('Опция отмены недоступна в режиме простого редактирования.')

        if count < 0:
            return False

        if count > self.edit_count:
            raise Exception(f'Для отмены доступно {self.edit_count} < {count} действий.')

        if count > 0:
            for i in range(count):
                self.history.pop()

            self.current_path = self.history[-1]
            self.edit_count -= count

        return self.current_path

