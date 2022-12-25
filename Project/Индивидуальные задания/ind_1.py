#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib


def add_plane(staff, destination, num, typ):
    """
    Добавить данные о самолете.
    """
    staff.append(
        {
            "destination": destination,
            "num": num,
            "typ": typ,
        }
    )
    return staff


def display_planes(staff):
    """
    Отобразить список самолетов.
    """
    # Проверить, что список самолетов не пуст.
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )
        print(line)

        # Вывести данные о всех самолетах.
        for idx, plane in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    plane.get('destination', ''),
                    plane.get('num', 0),
                    plane.get('typ', '')
                )
            )

        print(line)

    else:
        print("Список самолетов пуст")


def select_planes(staff, jet):
    """
    Выбрать самолеты с заданным типом.
    """
    # Сформировать список самолетов.
    result = [plane for plane in staff if jet == plane.get('typ', '')]

    # Возвратить список выбранных самолетов.
    return result


def save_planes(file_name, staff):
    """
    Сохранить все самолеты в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_planes(file_name):
    """
    Загрузить все самолеты из файла JSON.
    """

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("planes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new plane"
    )
    add.add_argument(
        "-d",
        "--destination",
        action="store",
        required=True,
        help="The plane's destination"
    )
    add.add_argument(
        "-n",
        "--num",
        action="store",
        type=int,
        required=True,
        help="The plane's numer"
    )
    add.add_argument(
        "-t",
        "--typ",
        action="store",
        required=True,
        help="The plane's type"
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all planes"
    )

    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the planes"
    )
    select.add_argument(
        "-T",
        "--type",
        action="store",
        required=True,
        help="The required type"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    args.filename = pathlib.Path.home().joinpath(args.filename)
    if os.path.exists(args.filename):
        planes = load_planes(args.filename)
    else:
        planes = []

    # Добавить работника.
    if args.command == "add":
        planes = add_plane(
            planes,
            args.destination,
            args.num,
            args.typ
        )
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        display_planes(planes)

    # Выбрать требуемых рааботников.
    elif args.command == "select":
        selected = select_planes(planes, args.type)
        display_planes(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_planes(args.filename, planes)


if __name__ == '__main__':
    main()