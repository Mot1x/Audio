import os
import subprocess


class FFmpeg:
    cmds = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    cmds_probe = 'C:\\ffmpeg\\bin\\ffprobe.exe'
    exts = ['wav', 'mp3']

    def __init__(self, file):
        self.file = file
        self.edit_count = 0

    def is_correct_file(self):
        if not os.path.exists(self.file):
            print(f"Ошибка: Файл {self.file} не найден.")
            return False

    def convert_to(self, ext, bitrate=16000):
        if self.file.endswith('mp3') or self.file.endswith('wav') and ext != self.file[:-3]:
            output_ext = FFmpeg.exts - self.file[:-3]
            output = f'{self.file[:-4]}.{output_ext}'
            process = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -acodec pcm_s16le -ac 1 -ar {bitrate} {output}')
            process.communicate()
            return output
        else:
            return False

    def cut(self, start=0, stop=0):
        if self.file.endswith('mp3') or self.file.endswith('wav'):
            output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            command = [FFmpeg.cmds, '-i', self.file, '-ss', start, '-to', stop, '-y', output]
            p = subprocess.Popen(command, stderr=subprocess.PIPE)
            p.communicate()
            self.edit_count += 1
            return output
        else:
            return False

    def volume(self, volume):
        if self.file.endswith('mp3') or self.file.endswith('wav'):
            if not os.path.exists(self.file):
                print(f"Ошибка: Файл {self.file} не найден.")
                return False
            output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            command = [FFmpeg.cmds, '-i', self.file, '-af', f'volume={volume}', '-y', output]
            p = subprocess.Popen(command, stderr=subprocess.PIPE)
            p.communicate()
            self.edit_count += 1
            return output
        else:
            return False

    def speed_up(self, speed):
        if self.file.endswith('wav') or self.file.endswith('mp3'):
            if os.path.exists(self.file):
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
            else:
                print(f"Ошибка: Файл {self.file} не найден.")
                return False
        #if self.file.endswith('mp3'):
            #output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            #p = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -af atempo={speed} {output}')
            #p.communicate()
            #self.edit_count += 1
            #return output
        else:
            return False
