if __name__ == "__main__":
    try:
        import sys
        import functions
        import argparse
        import os

        parser = argparse.ArgumentParser(description="Аудиоредактор")
        subparsers = parser.add_subparsers()

        #Команда convert
        parser_convert = subparsers.add_parser("convert", help="Преобразовывает формат")
        parser_convert.add_argument("audio", help="Вставьте аудио")
        parser_convert.add_argument("ext", help="Формат")
        parser_convert.add_argument("-b", help="Битрейт звука (по умолчанию 44100)", default=44100, type=int)
        parser_convert.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).convert_to(args.ext, args.b)))

        #Команда cut
        parser_cut = subparsers.add_parser("cut", help="Срез")
        parser_cut.add_argument("audio", help="Вставьте аудио")
        parser_cut.add_argument('start', help="Старт", default=0)
        parser_cut.add_argument('stop', help="Стоп", default=0)
        parser_cut.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).cut(args.start, args.stop)))

        # Команда volume
        parser_volume = subparsers.add_parser("volume", help="Изменение громкости")
        parser_volume.add_argument("audio", help="Вставьте аудио")
        parser_volume.add_argument("volume", help="Громкость")
        parser_volume.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).volume(args.volume)))

        # Команда speed
        parser_speed = subparsers.add_parser("speed", help="Изменение скорости")
        parser_speed.add_argument("audio", help="Вставьте аудио")
        parser_speed.add_argument("speed", help="Скорость")
        parser_speed.set_defaults(func=lambda args: print(functions.FFmpeg(args.audio).speed_up(args.speed)))

        # Обработка аргументов
        args = parser.parse_args()
        args.func(args)

    except Exception as e:
        print(f"Ошибка : {e}")
