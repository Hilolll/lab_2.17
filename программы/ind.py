import json
import sys
from jsonschema import validate, ValidationError

def get_route():
    """
    Запросить данные о списке
    """
    start = input("Ведите фамилию, имя ")
    finish = input("Введите знак Зодиака ")
    zodiac = (input("Введите дату рождения "))

    return {
        'start': start,
        'finish': finish,
        'zodiac': zodiac,
    }


def display_route(routes):
    """
    Отобразить список
    """
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^14} |'.format(
                "№",
                "Фамилия, имя",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)

        for idx, worker in enumerate(routes, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>14} |'.format(
                    idx,
                    worker.get('start', ''),
                    worker.get('finish', ''),
                    worker.get('zodiac', '')
                )
            )
        print(line)
    else:
        print("Список пуст")


def select_route(routes, period):
    """
    Выбрать зодиак
    """
    result = []
    for employee in routes:
        if employee.get('finish') == period:
            result.append(employee)

    return result


def save_routes(file_name, staff):
    """
    Сохранить данные в файл JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить данные из файла JSON
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "start": {"type": "string"},
                "finish": {"type": "string"},
                "zodiac": {"type": "string"},
            },
            "required": [
                "start",
                "finish",
                "zodiac",
            ],
        },
    }
    # Открыть файл с заданным именем и прочитать его содержимое.
    with open(file_name, "r") as file_in:
        data = json.load(file_in)  # Прочитать данные из файла

    try:
        # Валидация
        validate(instance=data, schema=schema)
        print("JSON валиден по схеме.")
    except ValidationError as e:
        print(f"Ошибка валидации: {e.message}")

    return data  # Вернуть загруженные и проверенные данные


def main():
    """
    Главная функция программы
    """
    routes = []

    while True:
        command = input(">>> ").lower()
        if command == 'exit':
            break

        elif command == 'add':
            route = get_route()
            routes.append(route)
            routes.sort(key=lambda item: int(item.get('zodiac', '').split('.')[2]))

        elif command == 'list':
            display_route(routes)

        elif command.startswith('select'):
            parts = command.split(' ', maxsplit=1)
            period = parts[1].strip()  # Получаем название знака Зодиака
            selected = select_route(routes, period)
            if selected:
                display_route(selected)
            else:
                print("Нет людей с таким знаком Зодиака.")

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_routes(file_name, routes)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            routes = load_routes(file_name)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить знак зодиака;")
            print("list - вывести список;")
            print("select <список знаков зодиака> - запросить данные о зодиаке;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()