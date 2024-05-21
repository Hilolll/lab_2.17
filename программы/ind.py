#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Условие:
# Для своего варианта лабораторной работы 2.16 необходимо дополнительно реализовать
# интерфейс командной строки (CLI).
# Вариант 15

import argparse
import os
import json
from typing import List, Dict, Tuple, Union

DateOfBirth = Tuple[int, int, int]
Person = Dict[str, Union[str, DateOfBirth]]


def load_people(filename: str) -> List[Person]:
    with open(filename, "r") as f:
        return json.load(f)


def save_people(filename: str, people: List[Person]) -> None:
    with open(filename, "w") as f:
        json.dump(people, f, indent=4, ensure_ascii=False)


def add_person(people: List[Person], name: str, surname: str, date_of_birth: str, zodiac_sign: str) -> List[Person]:
    person = {
        "name": name,
        "surname": surname,
        "date_of_birth": [int(part) for part in date_of_birth.split(".")],
        "zodiac_sign": zodiac_sign,
    }
    people.append(person)
    people.sort(key=lambda p: p["date_of_birth"])
    return people


def list_people(people: List[Person]) -> None:
    print("Список людей:")
    for person in people:
        print(f"{person['surname']} {person['name']} - {person['date_of_birth'][0]}.{person['date_of_birth'][1]}.{person['date_of_birth'][2]}")


def select_people(people: List[Person], month: int) -> None:
    print(f"Люди, родившиеся в {month} месяце:")
    for person in people:
        if person["date_of_birth"][1] == month:
            print(f"{person['surname']} {person['name']}")


def main():
    parser = argparse.ArgumentParser(description="Управление списком людей")
    subparsers = parser.add_subparsers(dest="command")

    # Создание парсера для добавления человека.
    parser_add = subparsers.add_parser('add', help="Добавить человека")
    parser_add.add_argument("-n", "--name", help="Имя человека")
    parser_add.add_argument("-s", "--surname", help="Фамилия человека")
    parser_add.add_argument("-d", "--date_of_birth", help="Дата рождения (формат ДД.ММ.ГГГГ)")
    parser_add.add_argument("-z", "--zodiac_sign", help="Знак зодиака")

    # Создание парсера для вывода списка людей.
    _ = subparsers.add_parser('list', help="Вывести список людей")

    # Создание парсера для выбора человека по месяцу рождения.
    parser_select = subparsers.add_parser('select', help="Выбрать людей по месяцу рождения")
    parser_select.add_argument("-m", "--month", type=int, help="Месяц рождения")

    # Разбираем аргументы командной строки.
    args = parser.parse_args()

    is_dirty = False

    filename = os.path.join("data", args.filename)

    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []

    # Определяем, какую команду нужно выполнить.
    if args.command == 'add':
        people = add_person(people, args.name, args.surname,
                            args.date_of_birth, args.zodiac_sign)
        is_dirty = True

    elif args.command == 'list':
        list_people(people)

    elif args.command == 'select':
        select_people(people, args.month)

    if is_dirty:
        save_people(filename, people)


if __name__ == "__main__":
    main()
