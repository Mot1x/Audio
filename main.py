if __name__ == "__main__":
    try:
        import sys
        import ffmpeg
        import functions
        import argparse
        import os

        parser = argparse.ArgumentParser(description="Аудиоредактор")
        subparsers = parser.add_subparsers()

        # Первая команда
        parser_find = subparsers.add_parser("название команды", help="Какая-то команда")
        parser_find.add_argument("audio", help="Вставьте аудио")
        parser_find.set_defaults(func=lambda args: print(functions.func(args.audio)))

        # Обработка аргументов
        args = parser.parse_args()
        args.func(args)

    except Exception as e:
        print(f"Ошибка : {e}")
