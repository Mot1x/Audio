import os
import subprocess


class FFmpeg:
    cmds = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    cmds_probe = 'C:\\ffmpeg\\bin\\ffprobe.exe'
    exts = ['wav', 'mp3']

    def __init__(self, file):
        self.file = file
        self.edit_count = 1

    def is_correct_file(self):
        if not os.path.exists(self.file):
            print(f"Ошибка: Файл {self.file} не найден.")
        return os.path.exists(self.file)

    def run_cmd(self, command):
        p = subprocess.Popen(command, stderr=subprocess.PIPE)
        p.communicate()
        self.edit_count += 1

    def set_output(self, ext=None):
        return f'{self.file[:-4]}.{ext}' if ext else f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'

    def convert_to(self, ext, bitrate):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts and ext in FFmpeg.exts:
            output = self.set_output(ext)
            command = [FFmpeg.cmds, '-i', self.file, '-ac', '2', '-ar', str(bitrate), '-y', output]
            self.run_cmd(command)
            return output
        else:
            return False

    def cut(self, start=None, stop=None):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()

            command = [FFmpeg.cmds, '-i', self.file]
            if start:
                command.extend(['-ss', start])
            if stop:
                command.extend(['-to', stop])
            command.extend(['-y', output])

            self.run_cmd(command)
            return output
        else:
            return False

    def volume(self, volume):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = self.set_output()
            command = [FFmpeg.cmds, '-i', self.file, '-af', f'volume={volume}', '-y', output]
            self.run_cmd(command)
            return output
        else:
            return False

    def speed_up(self, speed):
        if self.is_correct_file() and self.file[-3:] in FFmpeg.exts:
            output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            command = [FFmpeg.cmds, '-i', os.path.abspath(self.file), '-af', f'rubberband=tempo={speed}', '-y',
                       output]
            p = subprocess.Popen(command)
            p.wait()
            if p.returncode == 0:
                self.edit_count += 1
                return output
            else:
                if p.stderr:  # Проверяем, есть ли вывод в stderr
                    error_message = p.stderr.read().decode('utf-8', errors='ignore')
                    print(f"Ошибка при изменении скорости: {error_message}")
                else:
                    print("Ошибка при изменении скорости: Неизвестная ошибка.")
                return False
        # if self.file.endswith('mp3'):
        # output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
        # p = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -af atempo={speed} {output}')
        # p.communicate()
        # self.edit_count += 1
        # return output
        else:
            return False
