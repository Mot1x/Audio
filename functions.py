import subprocess
import sys

import additional_functions
from pathlib import Path


class FFmpeg:
    _cmds: Path = Path('C:\\ffmpeg\\bin\\ffmpeg.exe')
    _cmds_probe: Path = Path('C:\\ffmpeg\\bin\\ffprobe.exe')
    _exts: list[str] = additional_functions.exts

    def __init__(self, file: str, is_simple: bool):
        self._file: Path = Path(file)
        self._current_path: Path = Path(file)
        self._history: list[Path] = [Path(self._file)]
        self._redo_history: list[Path] = []
        self._is_simple: bool = is_simple

    def execute_in_window(self, command: str, *args):
        try:
            if command == 'quit':
                sys.exit()

            elif command == 'read_file':
                result = self.read_file(*args)

            elif command == 'help':
                result = self.help(*args)

            elif command in additional_functions.command_usage.keys():
                local_vars = {'file': self, 'args': args}
                exec(f'state = file.{command}(*args)', globals(), local_vars)
                state = local_vars.get('state')

                if state:
                    if command not in ['undo', 'redo']:
                        self._redo_history.clear()
                    result = f'Изменение выполнено. Ваш файл: {state}'
                else:
                    result = additional_functions.return_fail_message(command)
            else:
                result = f'{command} {" ".join(args)}: Такой команды нет. ' \
                         f'Существующие команды: {", ".join(additional_functions.command_usage.keys())}'

        except Exception as e:
            result = f"Ошибка: {e}" + "\n" + additional_functions.return_fail_message(command)

        return result
    
    def execute(self, command: str, req_args=None) -> None:
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
            else:
                print(f'{command} {" ".join(req_args)}: Такой команды нет. ' 
                      f'Существующие команды: {", ".join(additional_functions.command_usage.keys())}')

        except Exception as e:
            print(f"Ошибка: {e}")
            additional_functions.print_fail_message(command)

    def convert(self, ext=None, bitrate=44100) -> Path:
        f'Конвертирует аудиофайл в один из доступных форматов ({", ".join(FFmpeg._exts)}).'
        if additional_functions.is_correct_file_and_ext(self._current_path, ext):
            output: Path = additional_functions.set_output(self._file, ext)
            command: list[str] = [FFmpeg._cmds.resolve(),
                       '-i', self._current_path.resolve(),
                       '-ac', '2',
                       '-ar', str(bitrate),
                       '-y', output.resolve()]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def cut(self, start=None, stop=None) -> Path:
        """Обрезает аудио"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)

            command: list[str] = [FFmpeg._cmds.resolve(), '-i', self._current_path.resolve()]
            if start:
                command.extend(['-ss', start])
            if stop:
                command.extend(['-to', stop])
            command.extend(['-y', output.resolve()])

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def volume(self, volume=1) -> Path:
        """Изменение громкости"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [FFmpeg._cmds.resolve(),
                       '-i', self._current_path.resolve(),
                       '-af', f'volume={volume}',
                       '-y', output.resolve()]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def splice(self, other_file: str, side='r'):
        """Склейка текущего аудиофайла с другим с определеноой стороны"""
        other_file: Path = Path(other_file)
        if side not in ['r', 'l']:
            raise ValueError("Неверный параметр side: должен быть 'l' или 'r'")

        if (additional_functions.is_correct_file_and_ext(self._current_path) and
                additional_functions.is_correct_file_and_ext(other_file)):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [
                'ffmpeg',
                '-i', self._current_path.resolve() if side == 'r' else other_file.resolve(),
                '-i', other_file.resolve() if side == 'r' else self._current_path.resolve(),
                '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[outa]',
                '-map', '[outa]',
                output.resolve()
            ]
            
            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def overlay(self, other_file: str) -> Path:
        """Накладка другого файла на текущий"""
        other_file: Path = Path(other_file)
        if (additional_functions.is_correct_file_and_ext(self._current_path) and
                additional_functions.is_correct_file_and_ext(other_file)):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [
                'ffmpeg',
                '-i', self._current_path.resolve(),
                '-i', other_file.resolve(),
                '-filter_complex', 'amix=inputs=2',
                output.resolve()
            ]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def speed(self, speed=1) -> Path:
        """Изменение скорости, как ускорение, так и замедление"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [FFmpeg._cmds.resolve(),
                       '-i', self._current_path.resolve(),
                       '-af', f'rubberband=tempo={speed}',
                       '-y', output.resolve()]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output

    def fade_in(self, start, time) -> Path:
        """Постепенный набор полной громкости"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [FFmpeg._cmds.resolve(),
                "-i", self._current_path.resolve(),
                "-af", "afade=t=in:st=" + str(start) + ":d=" + str(time),
                '-y', output.resolve()]

        if additional_functions.run_cmd(command) == 0:
            self._add_to_history(output)
            return output

    def fade_out(self, start, time) -> Path:
        """Постепенный набор полной громкости"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)
            command: list[str] = [FFmpeg._cmds.resolve(),
                                  "-i", self._current_path.resolve(),
                                  "-af", "afade=t=out:st=" + str(start) + ":d=" + str(time),
                                  '-y', output.resolve()]

        if additional_functions.run_cmd(command) == 0:
            self._add_to_history(output)
            return output

    def resample_speed(self, speed=1) -> Path:
        """Изменение скорости с изменением тональности"""
        if additional_functions.is_correct_file_and_ext(self._current_path):
            output: Path = additional_functions.set_output(self._file)
            samplerate: int = self._get_samplerate()
            command: list[str] = [FFmpeg._cmds.resolve(),
                       '-i', self._current_path.resolve(),
                       '-af', f'asetrate={samplerate}*{speed},aresample={samplerate}',
                       '-y', output.resolve()]

            if additional_functions.run_cmd(command) == 0:
                self._add_to_history(output)
                return output
    
    def read_file(self, file: str) -> None:
        """Выполнение инструкций построчно из файла"""
        with open(file) as file_program:
            requests: list[str] = [request.strip() for request in file_program.readlines()]
            for request in requests:
                command, req_args = additional_functions.get_command_and_args(request)
                try:
                    self.execute(command, req_args)

                except Exception as e:
                    print(f"Ошибка: {e}")
                    additional_functions.print_fail_message(command)
            print(f"\nФайл {file} выполнен.")

    def render(self, path=None) -> Path:
        """Рендерит аудио"""
        if additional_functions.is_correct_file_and_ext(self._current_path) and path:
            command: list[str] = [FFmpeg._cmds.resolve(),
                       '-i', self._current_path.resolve(),
                       '-y', path]
            additional_functions.run_cmd(command)
            return Path(path)

    def help(self, command=None) -> str:
        """Вывод справки с командами"""
        comm_descr: dict = additional_functions.command_descriptions
        comm_us: dict = additional_functions.command_usage
        if not command:
            for command in comm_descr.keys():
                print(
                    f'{command} - {comm_descr[command]}\nИспользование: {comm_us[command]}\n')

        elif command in comm_descr.keys():
            return f'{command} - {comm_descr[command]}\nИспользование: {comm_us[command]}'

        else:
            return f'Такой команды нет. Существующие команды: {", ".join(comm_us.keys())}'

    def undo(self, count=1) -> Path | Exception:
        """Отмена изменений"""
        count: int = int(count)

        if self._is_simple:
            raise Exception('Опция отмены недоступна в режиме простого редактирования.')
        if count < 0:
            raise Exception(f'Отрицательное число изменения.')
        if count > len(self._history):
            raise Exception(f'Для отмены доступно {len(self._history)} < {count} действий.')
        for _ in range(count):
            self._redo_history.append(self._history.pop())

        self._current_path = self._history[-1]
        return self._current_path

    def redo(self, count=1) -> Path | Exception:
        """Возврат отменённых изменений"""
        count: int = int(count)

        if self._is_simple:
            raise Exception('Опция возврата недоступна в режиме простого редактирования.')
        if count < 0:
            raise Exception(f'Отрицательное число изменения.')
        if count > len(self._redo_history):
            raise Exception(f'Для возврата доступно {len(self._redo_history)} < {count} действий.')
        for _ in range(count):
            self._history.append(self._redo_history.pop())

        self._current_path = self._history[-1]
        return self._current_path

    def _add_to_history(self, output: Path) -> None:
        """Добавление в историю объекта нового output"""
        if not self._is_simple:
            self._current_path = output
            self._history.append(self._current_path)

    def _get_samplerate(self) -> int:
        """Получение частоты дискретизации"""
        command: list[str] = [
            FFmpeg._cmds_probe.resolve(), '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1', self._current_path.resolve()
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bitrate: str = result.stdout.decode('utf-8').strip()
        return int(bitrate)
