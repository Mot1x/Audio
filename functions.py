import os
import subprocess


class FFmpeg:
    cmds = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    cmds_probe = 'C:\\ffmpeg\\bin\\ffprobe.exe'
    exts = {'wav', 'mp3'}

    def __init__(self, file):
        self.file = file
        self.edit_count = 0

    def convert_to(self, ext, bitrate=16000):
        if self.file[:-3] in FFmpeg.exts and ext != self.file[:-3]:
            output_ext = FFmpeg.exts - self.file[:-3]
            output = f'{self.file[:-4]}.{output_ext}'
            process = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -acodec pcm_s16le -ac 1 -ar {bitrate} {output}')
            process.communicate()
            return output
        else:
            return False

    def cut(self, start=0, stop=0):
        if self.file[:-3] in FFmpeg.exts:
            output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            p = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -ss {start} -to {stop} {output}')
            p.communicate()
            self.edit_count += 1
            return output
        else:
            return False

    def volume(self, volume):
        if self.file[:-3] in FFmpeg.exts:
            output = f'{self.file[:-4]} ({self.edit_count}){self.file[-4:]}'
            p = subprocess.Popen(f'{FFmpeg.cmds} -i {self.file} -filter:a "volume={volume}" {output}')
            p.communicate()
            self.edit_count += 1
            return output
        else:
            return False
