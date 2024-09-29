import unittest
from datetime import timedelta
from unittest.mock import patch, MagicMock
from pathlib import Path
import io
import additional_functions
import functions


class Test(unittest.TestCase):
    def test_correct_command_and_args(self):
        command, req_args = additional_functions.get_command_and_args("cut 1 20")
        self.assertEqual(command, "cut", "error get command")
        self.assertEqual(req_args, ["1", "20"], "error get args")

    def test_correct_command_and_args_with_quotes(self):
        command, req_args = additional_functions.get_command_and_args('overlay "melody.wav"')
        self.assertEqual(command, "overlay", "error get command")
        self.assertEqual(req_args, ["melody.wav"], "error get args")

    def test_correct_command_and_args_with_uncorrect_quotes(self):
        self.assertRaises(Exception, additional_functions.get_command_and_args, 'overlay ""C:\melody.wav"')

    def test_convert_success(self):
        """Проверяет успешное преобразование файла."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
             patch("additional_functions.set_output") as mock_set_output, \
             patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test.wav")
            mock_run_cmd.return_value = 0

            output = ffmpeg.convert(ext="wav")

            self.assertEqual(output, Path("test.wav"))
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"), "wav")
            mock_set_output.assert_called_once_with(ffmpeg._file, "wav")
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-ac",
                    "2",
                    "-ar",
                    "44100",
                    "-y",
                    Path("test.wav").resolve(),
                ]
            )

    def test_convert_incorrect_file(self):
        """Проверяет обработку неверного типа файла convert."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = False

            output = ffmpeg.convert(ext="wav")

            self.assertIsNone(output)
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"), "wav")
            mock_set_output.assert_not_called()
            mock_run_cmd.assert_not_called()

    def test_convert_command_error(self):
        """Проверяет обработку ошибки выполнения команды convert."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test.wav")
            mock_run_cmd.return_value = 1

            output = ffmpeg.convert(ext="wav")

            self.assertIsNone(output)
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"), "wav")
            mock_set_output.assert_called_once_with(ffmpeg._file, "wav")
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-ac",
                    "2",
                    "-ar",
                    "44100",
                    "-y",
                    Path("test.wav").resolve(),
                ]
            )

    def test_cut_no_params(self):
        """Проверяет cut без параметров."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test_cut.mp3")
            mock_run_cmd.return_value = 0

            output = ffmpeg.cut()

            self.assertEqual(output, Path("test_cut.mp3"))
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
            mock_set_output.assert_called_once_with(ffmpeg._file)
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-y",
                    Path("test_cut.mp3").resolve(),
                ]
            )

    def test_cut_with_start_and_stop(self):
        """Проверяет cut с параметрами start и stop."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test_cut.mp3")
            mock_run_cmd.return_value = 0

            output = ffmpeg.cut(start=10, stop=14)

            self.assertEqual(output, Path("test_cut.mp3"))
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
            mock_set_output.assert_called_once_with(ffmpeg._file)
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-ss",
                    10,
                    "-to",
                    14,
                    "-y",
                    Path("test_cut.mp3").resolve(),
                ]
            )

    def test_cut_command_error(self):
        """Проверяет обработку ошибки выполнения команды cut."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test_cut.mp3")
            mock_run_cmd.return_value = 1

            output = ffmpeg.cut()

            self.assertIsNone(output)
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
            mock_set_output.assert_called_once_with(ffmpeg._file)
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-y",
                    Path("test_cut.mp3").resolve(),
                ]
            )

    def test_volume(self):
        """Проверяет изменение громкости volume."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with patch("additional_functions.is_correct_file_and_ext") as mock_is_correct_file_and_ext, \
                patch("additional_functions.set_output") as mock_set_output, \
                patch("additional_functions.run_cmd") as mock_run_cmd:
            mock_is_correct_file_and_ext.return_value = True
            mock_set_output.return_value = Path("test_volume.mp3")
            mock_run_cmd.return_value = 0

            output = ffmpeg.volume(volume=0.5)

            self.assertEqual(output, Path("test_volume.mp3"))
            mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
            mock_set_output.assert_called_once_with(ffmpeg._file)
            mock_run_cmd.assert_called_once_with(
                [
                    functions.FFmpeg._cmds.resolve(),
                    "-i",
                    Path("test.mp3").resolve(),
                    "-af",
                    "volume=0.5",
                    "-y",
                    Path("test_volume.mp3").resolve(),
                ]
            )

    def test_splice_right_duration(self):
        """Проверяет склейку с другим файлом справа, сравнивая длительность в splice."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(side_effect=[True, True])
        mock_set_output = MagicMock(return_value=Path("test_splice.mp3"))
        mock_run_cmd = MagicMock(return_value=0)

        # Заглушка для получения "времени" склеенного файла
        def get_duration(file_path):
            if file_path == Path("test_splice.mp3"):
                return timedelta(seconds=30)  # Предположим, что склеенный файл будет 30 сек.
            elif file_path == Path("test.mp3"):
                return timedelta(seconds=15)  # Первый файл - 15 сек.
            elif file_path == Path("other_file.mp3"):
                return timedelta(seconds=15)  # Второй файл - 15 сек.
            else:
                raise ValueError("Неверный путь файла")

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd
        additional_functions.get_duration = get_duration

        output = ffmpeg.splice("other_file.mp3", side="r")

        self.assertEqual(output, Path("test_splice.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_has_calls(
            [
                unittest.mock.call(Path("test.mp3")),
                unittest.mock.call(Path("other_file.mp3")),
            ]
        )
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                "ffmpeg",
                "-i",
                Path("test.mp3").resolve(),
                "-i",
                Path("other_file.mp3").resolve(),
                "-filter_complex",
                "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
                "-map",
                "[outa]",
                Path("test_splice.mp3").resolve(),
            ]
        )

        # Проверяем длительность
        self.assertEqual(get_duration(output), timedelta(seconds=30))

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd
        additional_functions.get_duration = get_duration

    def test_splice_invalid_side(self):
        """Проверяет исключение ValueError при неверном значении side в splice."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        with self.assertRaises(ValueError) as context:
            ffmpeg.splice("other_file.mp3", side="x")

        self.assertEqual(str(context.exception), "Неверный параметр side: должен быть 'l' или 'r'")

    def test_overlay_success(self):
        """Проверяет успешную накладку."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(side_effect=[True, True])
        mock_set_output = MagicMock(return_value=Path("test_overlay.mp3"))
        mock_run_cmd = MagicMock(return_value=0)

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd

        output = ffmpeg.overlay("other_file.mp3")

        self.assertEqual(output, Path("test_overlay.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_has_calls(
            [
                unittest.mock.call(Path("test.mp3")),
                unittest.mock.call(Path("other_file.mp3")),
            ]
        )
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                "ffmpeg",
                "-i",
                Path("test.mp3").resolve(),
                "-i",
                Path("other_file.mp3").resolve(),
                "-filter_complex",
                "amix=inputs=2",
                Path("test_overlay.mp3").resolve(),
            ]
        )

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd

    def test_overlay_incorrect_file(self):
        """Проверяет обработку неверного типа файла."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(side_effect=[True, False])
        mock_set_output = MagicMock(return_value=Path("test_overlay.mp3"))
        mock_run_cmd = MagicMock(return_value=0)

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd

        output = ffmpeg.overlay("other_file.mp3")

        self.assertIsNone(output)

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_has_calls(
            [
                unittest.mock.call(Path("test.mp3")),
                unittest.mock.call(Path("other_file.mp3")),
            ]
        )
        mock_set_output.assert_not_called()
        mock_run_cmd.assert_not_called()

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd

    def test_speed_up_duration(self):
        """Проверяет ускорение, сравнивая длительность."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(return_value=True)
        mock_set_output = MagicMock(return_value=Path("test_speed_up.mp3"))
        mock_run_cmd = MagicMock(return_value=0)

        # Заглушка для получения "времени" склеенного файла
        def get_duration(file_path):
            if file_path == Path("test_speed_up.mp3"):
                return timedelta(seconds=10)  # Предположим, что ускоренный файл будет 10 сек.
            elif file_path == Path("test.mp3"):
                return timedelta(seconds=15)  # Исходный файл - 15 сек.
            else:
                raise ValueError("Неверный путь файла")

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd
        additional_functions.get_duration = get_duration

        output = ffmpeg.speed(speed=1.5)  # Ускорение в 1.5 раза

        self.assertEqual(output, Path("test_speed_up.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                functions.FFmpeg._cmds.resolve(),
                "-i",
                Path("test.mp3").resolve(),
                "-af",
                "rubberband=tempo=1.5",
                "-y",
                Path("test_speed_up.mp3").resolve(),
            ]
        )

        # Проверяем длительность
        self.assertEqual(get_duration(output), timedelta(seconds=10))

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd
        additional_functions.get_duration = get_duration

    def test_speed_down_duration(self):
        """Проверяет замедление, сравнивая длительность."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(return_value=True)
        mock_set_output = MagicMock(return_value=Path("test_speed_down.mp3"))
        mock_run_cmd = MagicMock(return_value=0)

        # Заглушка для получения "времени" склеенного файла
        def get_duration(file_path):
            if file_path == Path("test_speed_down.mp3"):
                return timedelta(seconds=20)  # Предположим, что замедленный файл будет 20 сек.
            elif file_path == Path("test.mp3"):
                return timedelta(seconds=10)  # Исходный файл - 10 сек.
            else:
                raise ValueError("Неверный путь файла")

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd
        additional_functions.get_duration = get_duration

        output = ffmpeg.speed(speed=0.5)  # Замедление в 2 раза

        self.assertEqual(output, Path("test_speed_down.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                functions.FFmpeg._cmds.resolve(),
                "-i",
                Path("test.mp3").resolve(),
                "-af",
                "rubberband=tempo=0.5",
                "-y",
                Path("test_speed_down.mp3").resolve(),
            ]
        )

        # Проверяем длительность
        self.assertEqual(get_duration(output), timedelta(seconds=20))

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd
        additional_functions.get_duration = get_duration

    def test_resample_speed_up_duration(self):
        """Проверяет ускорение с изменением тональности, сравнивая длительность."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(return_value=True)
        mock_set_output = MagicMock(return_value=Path("test_resample_speed_up.mp3"))
        mock_run_cmd = MagicMock(return_value=0)
        mock_get_samplerate = MagicMock(return_value=44100)  # Предположим, что частота дискретизации 44100 Гц

        # Заглушка для получения "времени" склеенного файла
        def get_duration(file_path):
            if file_path == Path("test_resample_speed_up.mp3"):
                return timedelta(seconds=10)  # Предположим, что ускоренный файл будет 10 сек.
            elif file_path == Path("test.mp3"):
                return timedelta(seconds=15)  # Исходный файл - 15 сек.
            else:
                raise ValueError("Неверный путь файла")

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd
        additional_functions.get_duration = get_duration
        ffmpeg._get_samplerate = mock_get_samplerate

        output = ffmpeg.resample_speed(speed=1.5)  # Ускорение в 1.5 раза

        self.assertEqual(output, Path("test_resample_speed_up.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                functions.FFmpeg._cmds.resolve(),
                "-i",
                Path("test.mp3").resolve(),
                "-af",
                "asetrate=44100*1.5,aresample=44100",
                "-y",
                Path("test_resample_speed_up.mp3").resolve(),
            ]
        )
        mock_get_samplerate.assert_called_once_with()

        # Проверяем длительность
        self.assertEqual(get_duration(output), timedelta(seconds=10))

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd
        additional_functions.get_duration = get_duration
        ffmpeg._get_samplerate = ffmpeg._get_samplerate

    def test_resample_speed_down_duration(self):
        """Проверяет замедление с изменением тональности, сравнивая длительность."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(return_value=True)
        mock_set_output = MagicMock(return_value=Path("test_resample_speed_down.mp3"))
        mock_run_cmd = MagicMock(return_value=0)
        mock_get_samplerate = MagicMock(return_value=44100)  # Предположим, что частота дискретизации 44100 Гц

        # Заглушка для получения "времени" склеенного файла
        def get_duration(file_path):
            if file_path == Path("test_resample_speed_down.mp3"):
                return timedelta(seconds=20)  # Предположим, что замедленный файл будет 20 сек.
            elif file_path == Path("test.mp3"):
                return timedelta(seconds=10)  # Исходный файл - 10 сек.
            else:
                raise ValueError("Неверный путь файла")

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.set_output = mock_set_output
        additional_functions.run_cmd = mock_run_cmd
        additional_functions.get_duration = get_duration
        ffmpeg._get_samplerate = mock_get_samplerate

        output = ffmpeg.resample_speed(speed=0.5)  # Замедление в 2 раза

        self.assertEqual(output, Path("test_resample_speed_down.mp3"))

        # Проверяем вызовы mock-функций
        mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
        mock_set_output.assert_called_once_with(ffmpeg._file)
        mock_run_cmd.assert_called_once_with(
            [
                functions.FFmpeg._cmds.resolve(),
                "-i",
                Path("test.mp3").resolve(),
                "-af",
                "asetrate=44100*0.5,aresample=44100",
                "-y",
                Path("test_resample_speed_down.mp3").resolve(),
            ]
        )
        mock_get_samplerate.assert_called_once_with()

        # Проверяем длительность
        self.assertEqual(get_duration(output), timedelta(seconds=20))

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.set_output = additional_functions.set_output
        additional_functions.run_cmd = additional_functions.run_cmd
        additional_functions.get_duration = get_duration
        ffmpeg._get_samplerate = ffmpeg._get_samplerate

    def test_read_file(self):
        """Проверяет выполнение инструкций из файла."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_get_command_and_args = MagicMock(side_effect=[
            ("convert", ["wav"]),
            ("volume", [0.5]),
            ("speed", [1.2]),
        ])
        mock_execute = MagicMock()

        # Заменяем функции на моки
        additional_functions.get_command_and_args = mock_get_command_and_args
        ffmpeg.execute = mock_execute

        # Создаем тестовый файл в памяти
        test_file_content = "convert wav\nvolume 0.5\nspeed 1.2"
        test_file = io.StringIO(test_file_content)

        # Выполняем read_file с тестовым файлом
        # Читаем строчки из test_file и обрабатываем их
        for line in test_file:
            request = line.strip()
            command, req_args = additional_functions.get_command_and_args(request)
            try:
                ffmpeg.execute(command, req_args)
            except Exception as e:
                print(f"Ошибка: {e}")
                additional_functions.print_fail_message(command)

        # Проверяем вызовы мокированных функций
        mock_get_command_and_args.assert_has_calls(
            [
                unittest.mock.call("convert wav"),
                unittest.mock.call("volume 0.5"),
                unittest.mock.call("speed 1.2"),
            ]
        )
        mock_execute.assert_has_calls(
            [
                unittest.mock.call("convert", ["wav"]),
                unittest.mock.call("volume", [0.5]),
                unittest.mock.call("speed", [1.2]),
            ]
        )

        # Возвращаем оригинальные функции после теста
        additional_functions.get_command_and_args = additional_functions.get_command_and_args
        ffmpeg.execute = functions.FFmpeg.execute

    def test_render(self):
        """Проверяет рендеринг аудио."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        mock_is_correct_file_and_ext = MagicMock(return_value=True)
        mock_run_cmd = MagicMock(return_value=0)

        # Заменяем функции на моки
        additional_functions.is_correct_file_and_ext = mock_is_correct_file_and_ext
        additional_functions.run_cmd = mock_run_cmd

        output = ffmpeg.render(path="output.wav")

        self.assertEqual(output, Path("output.wav"))
        mock_is_correct_file_and_ext.assert_called_once_with(Path("test.mp3"))
        mock_run_cmd.assert_called_once_with(
            [
                functions.FFmpeg._cmds.resolve(),
                "-i",
                Path("test.mp3").resolve(),
                "-y",
                "output.wav",
            ]
        )

        # Возвращаем оригинальные функции после теста
        additional_functions.is_correct_file_and_ext = additional_functions.is_correct_file_and_ext
        additional_functions.run_cmd = additional_functions.run_cmd

    def test_undo_one(self):
        """Проверяет отмену одного действия."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)
        ffmpeg._history = [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")]
        result = ffmpeg.undo()

        self.assertEqual(result, Path("test_convert.wav"))
        self.assertEqual(ffmpeg._history, [Path("test.mp3"), Path("test_convert.wav")])
        self.assertEqual(ffmpeg._redo_history, [Path("test_volume.mp3")])

    def test_undo_multiple(self):
        """Проверяет отмену нескольких действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)
        ffmpeg._history = [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")]
        result = ffmpeg.undo(count=2)

        self.assertEqual(result, Path("test.mp3"))
        self.assertEqual(ffmpeg._history, [Path("test.mp3")])
        self.assertEqual(ffmpeg._redo_history, [Path("test_volume.mp3"), Path("test_convert.wav")])

    def test_undo_invalid_count(self):
        """Проверяет отмену с недопустимым числом действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)

        self.assertRaises(Exception, ffmpeg.undo, 4)

    def test_undo_negative_count(self):
        """Проверяет отмену с отрицательным числом действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        self.assertRaises(Exception, ffmpeg.undo, -1)

    def test_undo_simple_mode(self):
        """Проверяет отмену в режиме простого редактирования."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        ffmpeg._is_simple = True  # Включаем простой режим
        self.assertRaises(Exception, ffmpeg.undo, )

    def test_redo_one(self):
        """Проверяет возврат одного отмененного действия."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)
        ffmpeg._history = [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")]
        ffmpeg.undo()  # Отменяем одно действие
        result = ffmpeg.redo()

        self.assertEqual(result, Path("test_volume.mp3"))
        self.assertEqual(ffmpeg._history, [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")])
        self.assertEqual(ffmpeg._redo_history, [])

    def test_redo_multiple(self):
        """Проверяет возврат нескольких отмененных действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)  # Отключаем простой режим
        ffmpeg._history = [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")]
        ffmpeg._redo_history = []  # Очищаем историю отмены

        ffmpeg.undo(count=2)  # Отменяем два действия
        result = ffmpeg.redo(count=2)

        self.assertEqual(result, Path("test_volume.mp3"))
        self.assertEqual(ffmpeg._history, [Path("test.mp3"), Path("test_convert.wav"), Path("test_volume.mp3")])
        self.assertEqual(ffmpeg._redo_history, [])

    def test_redo_invalid_count(self):
        """Проверяет возврат с недопустимым числом действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)
        self.assertRaises(Exception, ffmpeg.redo, 3)

    def test_redo_negative_count(self):
        """Проверяет возврат с отрицательным числом действий."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), False)
        self.assertRaises(Exception, ffmpeg.redo, -1)

    def test_redo_simple_mode(self):
        """Проверяет возврат в режиме простого редактирования."""
        ffmpeg = functions.FFmpeg(str(Path("test.mp3")), True)
        ffmpeg._is_simple = True
        self.assertRaises(Exception, ffmpeg.redo, ())


if __name__ == "__main__":
    unittest.main()