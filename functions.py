import os
import subprocess
import sys

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
        'redo': f'Возврат отменённых изменений.',
        'quit': f'Выход из утилиты.',
        'help': f'Справка по командам.',
        'splice': f'Склейка текущего и другого файлов',
        'overlay': f'Накладка другого файла',
        'read_file': f'Чтение инструкций из файла',
        'resample_speed': f'Второй способ ускорения'
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
                f'тогда будет выведена справка обо всех коммандах',
        'splice': f'splice [other_file] [side], где other_file - путь к другому файлу, side - r или l'
                  f'(справа или слева присоединение другого файла)',
        'overlay': f'overlay [other_file], где other_file - путь к другому файлу',
        'read_file': f'read_file [Путь к файлу с инструкцией]',
        'resample_speed': f'resample_speed [скорость]'
    }

    def __init__(self, file, is_simple):
        self.file = file
        self.current_path = file
        self.history = [self.file]
        self.redo_history = []
        self.is_simple = is_simple
    
    def execute(self, command, req_args=None):
        try:
            if command == 'quit':
                sys.exit()

            elif command == 'read_file':
                self.read_file(*req_args)
                
            elif command == 'help':
                self.help(*req_args)

            elif command in self.command_usage.keys():
                local_vars = {'file': self, 'req_args': req_args}
                exec(f'state = file.{command}(*req_args)', globals(), local_vars)
                state = local_vars.get('state')

                if state:
                    if command not in ['undo', 'redo']:
                        self.redo_history.clear()
                    print(f'Ваш файл: {state}')
                else:
                    FFmpeg.print_fail_message(command)

            else:
                print(f'{command} {" ".join(req_args)}: Такой команды нет.' 
                      f'Существующие команды: {", ".join(self.command_usage.keys())}')

        except Exception as e:
            print(f"Ошибка: {e}")
            FFmpeg.print_fail_message(command)
    
    def is_correct_file(self):
        if not os.path.exists(self.file):
            print(f"Ошибка: Файл {self.file} не найден.")
        return os.path.exists(self.file)
    
    @staticmethod
    def get_command_and_args(request):
        command_and_args = request.split(" ")
        command = command_and_args[0]
        args = command_and_args[1:]
        return command, args
    
    @staticmethod
    def print_fail_message(command):
        if command == '':
            print(f'Не было дано команды.')
        else:
            print(
                f'Команда не выполнилась. Проверьте существование файла и разрешение '
                f'(подходящие разрешения: {", ".join(FFmpeg.exts)}), а также аргументы.\n'
                f'Использование команды: {FFmpeg.command_usage[command]}')  # перенести
    
    def run_cmd(self, command):
        p = subprocess.Popen(command, stderr=subprocess.PIPE)
        p.communicate()
        p.wait()
        return p.returncode

    def add_to_history(self, output):
        if not self.is_simple:
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

    def convert(self, ext=None, bitrate=44100):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and ext in FFmpeg.exts:
            output = self.set_output(ext)
            command = [FFmpeg.cmds,
                       '-i', self.current_path,
                       '-ac', '2',
                       '-ar', str(bitrate),
                       '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output

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

        return False

    def volume(self, volume=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds,
                       '-i', self.current_path,
                       '-af', f'volume={volume}',
                       '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output

        return False

    def splice(self, other_file, side='r'):
        if side not in ['r', 'l']:
            raise ValueError("Неверный параметр side: должен быть 'l' или 'r'")

        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [
                'ffmpeg',
                '-i', self.current_path if side == 'r' else other_file,
                '-i', other_file if side == 'r' else self.current_path,
                '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[outa]',
                '-map', '[outa]',
                output
            ]
            
            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output

        return False

    def overlay(self, other_file):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [
                'ffmpeg',
                '-i', os.path.abspath(self.current_path),
                '-i', other_file,
                '-filter_complex', '[0:a][1:a]amix=inputs=2',
                '-map', '[out]',
                output
            ]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output

        return False

    def speed(self, speed=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds,
                       '-i', os.path.abspath(self.current_path),
                       '-af', f'rubberband=tempo={speed}',
                       '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output
            
        return False

    def resample_speed(self, speed=1):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            samplerate = self.get_samplerate()
            command = [FFmpeg.cmds,
                       '-i', self.current_path,
                       '-af', f'asetrate={samplerate}*{speed},aresample={samplerate}',
                       '-y', output]

            if self.run_cmd(command) == 0:
                self.add_to_history(output)
                return output

        return False
    
    def read_file(self, file):
        with open(file) as file_program:
            requests = [request.strip() for request in file_program.readlines()]
            for request in requests:
                command, req_args = FFmpeg.get_command_and_args(request)
                try:
                    self.execute(command, req_args)

                except Exception as e:
                    print(f"Ошибка: {e}")
                    FFmpeg.print_fail_message(command)
            print(f"\nФайл {file} выполнен.")

    def get_samplerate(self):
        command = [
            FFmpeg.cmds_probe, '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1', self.current_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bitrate = result.stdout.decode('utf-8').strip()
        return int(bitrate)

    def render(self, path=None):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and path:
            command = [FFmpeg.cmds, '-i', self.current_path, '-y', path]
            self.run_cmd(command)
            return path
        
        return False

    def help(self, command=None):
        if not command:
            for command in self.command_descriptions.keys():
                print(
                    f'{command} - {self.command_descriptions[command]}\nИспользование: {self.command_usage[command]}\n')

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
        if count > len(self.history):
            raise Exception(f'Для отмены доступно {len(self.history)} < {count} действий.')
        for i in range(count):
            self.redo_history.append(self.history.pop())

        self.current_path = self.history[-1]
        return self.current_path

    def redo(self, count=1):
        count = int(count)

        if self.is_simple:
            raise Exception('Опция возврата недоступна в режиме простого редактирования.')
        if count < 0:
            return False
        if count > len(self.redo_history):
            raise Exception(f'Для возврата доступно {len(self.redo_history)} < {count} действий.')
        for i in range(count):
            self.history.append(self.redo_history.pop())

        self.current_path = self.history[-1]
        return self.current_path

