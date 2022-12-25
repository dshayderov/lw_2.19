#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import collections
import pathlib
from datetime import datetime


def tree(directory):
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = ' ' * depth
        print(f'{spacer}+ {path.name}')


def main(command_line=None):
    directory = pathlib.Path.cwd()
    file_parser = argparse.ArgumentParser(add_help=False)

    # Создаем основной парсер командной строки
    parser = argparse.ArgumentParser("tree")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создаем субпарсер для создания новой папки
    createdir = subparsers.add_parser(
        "mkdir",
        parents=[file_parser]
    )
    createdir.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для удаления папок
    removedir = subparsers.add_parser(
        "rmdir",
        parents=[file_parser]
    )
    removedir.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для создания файлов
    createfile = subparsers.add_parser(
        "mkfile",
        parents=[file_parser]
    )
    createfile.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для удаления файлов
    removefile = subparsers.add_parser(
        "rmfile",
        parents=[file_parser]
    )
    removefile.add_argument(
        "filename",
        action="store"
    )

    count = subparsers.add_parser(
        "count",
        parents=[file_parser]
    )

    last = subparsers.add_parser(
        "last",
        parents=[file_parser]
    )

    args = parser.parse_args(command_line)

    if args.command == 'mkdir':
        directory_path = directory / args.filename
        directory_path.mkdir()
        tree(directory)

    elif args.command == "rmdir":
        directory_path = directory / args.filename
        directory_path.rmdir()
        tree(directory)

    elif args.command == "mkfile":
        directory_path = directory / args.filename
        directory_path.touch()
        tree(directory)

    elif args.command == "rmfile":
        directory_path = directory / args.filename
        directory_path.unlink()
        tree(directory)

    elif args.command == "count":
        print(collections.Counter(p.suffix for p in directory.iterdir()))

    elif args.command == "last":
        time, file = max((f.stat().st_mtime, f) for f in directory.iterdir())
        print(datetime.fromtimestamp(time), file.name)

    else:
        tree(directory)


if __name__ == "__main__":
    main()