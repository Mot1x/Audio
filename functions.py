import os
import subprocess
import sys
import additional_functions


class FFmpeg:
    _cmds = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    _cmds_probe = 'C:\\ffmpeg\\bin\\ffprobe.exe'
    _exts = additional_functions.exts

    def __init__(self, file, is_simple):
        self._file = file
        self._current_path = file
        self._history = [self._file]
        self._redo_history = []
        self._is_simple = is_simple
    
    def execute(self, command, req_args=None):
        """Выполнение command"""
        try:
            if command == 'quit':
                sys.exit()

            elif command == 'read_file':
                self.read_file(*req_args)
                
            elif command == 'help':
                self.help(*req_args)

            elif command in additional_functions.command_usage.keys():
                local_vars = {'file': self, 'req_args': req_args}
                exec(f'state = file.{command}(*req_args)', globals(), local_vars)
                state = local_vars.get('state')

                if state:
                    if command not in ['undo', 'redo']:
                        self._redo_history.clear()
                    print(f'Ваш файл: {state}')
                    return

                additional_functions.print_fail_message(command)
                return

            print(f'{command} {" ".join(req_args)}: Такой команды нет.' 
                  f'Существующие команды: {", ".join(additional_functions.command_usage.keys())}')

        except Exception as e:
            print(f"Ошибка: {e}")
            additional_functions.print_fail_message(command)

    def convert(self, ext=None, bitrate=44100):
        f'Конвертирует аудиофайл в один из доступных форматов ({", ".join(FFmpeg._exts)}).'
        if additional_functions.is_correct_file_and_ext(self._file, ext):
            output = additional_functions.set_output(self._file, ext)
            command = [FFmpeg._cmds,
                       '-i', self._current_path,
                       '-ac', '2',
                       '-ar', str(bitrate),
                       '-y', output]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def cut(self, start=None, stop=None):
        """Обрезает аудио"""
        if additional_functions.is_correct_file_and_ext(self._file):
            output = additional_functions.set_output(self._file)

            command = [FFmpeg._cmds, '-i', self._current_path]
            if start:
                command.extend(['-ss', start])
            if stop:
                command.extend(['-to', stop])
            command.extend(['-y', output])

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def volume(self, volume=1):
        """Изменение громкости"""
        if additional_functions.is_correct_file_and_ext(self._file):
            output = additional_functions.set_output(self._file)
            command = [FFmpeg._cmds,
                       '-i', self._current_path,
                       '-af', f'volume={volume}',
                       '-y', output]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def splice(self, other_file, side='r'):
        """Склейка текущего аудиофайла с другим с определеноой стороны"""
        if side not in ['r', 'l']:
            raise ValueError("Неверный параметр side: должен быть 'l' или 'r'")

        if (additional_functions.is_correct_file_and_ext(self._file) and
                additional_functions.is_correct_file(other_file)):
            output = additional_functions.set_output(self._file)
            command = [
                'ffmpeg',
                '-i', self._current_path if side == 'r' else other_file,
                '-i', other_file if side == 'r' else self._current_path,
                '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[outa]',
                '-map', '[outa]',
                output
            ]
            
            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def overlay(self, other_file):
        """Накладка другого файла на текущий"""
        if (additional_functions.is_correct_file_and_ext(self._file) and
                additional_functions.is_correct_file(other_file)):
            output = additional_functions.set_output(self._file)
            command = [
                'ffmpeg',
                '-i', os.path.abspath(self._current_path),
                '-i', other_file,
                '-filter_complex', '[0:a][1:a]amix=inputs=2',
                '-map', '[out]',
                output
            ]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def speed(self, speed=1):
        """Изменение скорости, как ускорение, так и замедление"""
        if additional_functions.is_correct_file_and_ext(self._file):
            output = additional_functions.set_output(self._file)
            command = [FFmpeg._cmds,
                       '-i', os.path.abspath(self._current_path),
                       '-af', f'rubberband=tempo={speed}',
                       '-y', output]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def resample_speed(self, speed=1):
        """Изменение скорости с изменением тональности"""
        if additional_functions.is_correct_file_and_ext(self._file):
            output = additional_functions.set_output(self._file)
            samplerate = self._get_samplerate()
            command = [FFmpeg._cmds,
                       '-i', self._current_path,
                       '-af', f'asetrate={samplerate}*{speed},aresample={samplerate}',
                       '-y', output]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output
    
    def read_file(self, file):
        """Выполнение инструкций построчно из файла"""
        with open(file) as file_program:
            requests = [request.strip() for request in file_program.readlines()]
            for request in requests:
                command, req_args = additional_functions.get_command_and_args(request)
                try:
                    self.execute(command, req_args)

                except Exception as e:
                    print(f"Ошибка: {e}")
                    additional_functions.print_fail_message(command)
            print(f"\nФайл {file} выполнен.")

    def render(self, path=None):
        """Редрерит аудио"""
        if additional_functions.is_correct_file_and_ext(self._file) and path:
            command = [FFmpeg._cmds, '-i', self._current_path, '-y', path]
            additional_functions.run_cmd(command)
            return path
        
        return False

    def help(self, command=None):
        """Вывод справки с командами"""
        comm_descr = additional_functions.command_descriptions
        comm_us = additional_functions.command_usage
        if not command:
            for command in comm_descr.keys():
                print(
                    f'{command} - {comm_descr[command]}\nИспользование: {comm_us[command]}\n')

        elif command in comm_descr.keys():
            print(f'{command} - {comm_descr[command]}\nИспользование: {comm_us[command]}')

        else:
            print(f'Такой команды нет. Существующие команды: {", ".join(comm_us.keys())}')

    def undo(self, count=1):
        """Отмена изменений"""
        count = int(count)

        if self._is_simple:
            raise Exception('Опция отмены недоступна в режиме простого редактирования.')
        if count < 0:
            return False
        if count > len(self._history):
            raise Exception(f'Для отмены доступно {len(self._history)} < {count} действий.')
        for _ in range(count):
            self._redo_history.append(self._history.pop())

        self._current_path = self._history[-1]
        return self._current_path

    def redo(self, count=1):
        """Возврат отменённых изменений"""
        count = int(count)

        if self._is_simple:
            raise Exception('Опция возврата недоступна в режиме простого редактирования.')
        if count < 0:
            return False
        if count > len(self._redo_history):
            raise Exception(f'Для возврата доступно {len(self._redo_history)} < {count} действий.')
        for _ in range(count):
            self._history.append(self._redo_history.pop())

        self._current_path = self._history[-1]
        return self._current_path

    def _add_to_history(self, output):
        """Добавление в историю объекта нового output"""
        if not self._is_simple:
            self._current_path = output
            self._history.append(self._current_path)

    def _get_samplerate(self):
        """Получение частоты дискретизации"""
        command = [
            FFmpeg._cmds_probe, '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1', self._current_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bitrate = result.stdout.decode('utf-8').strip()
        return int(bitrate)
