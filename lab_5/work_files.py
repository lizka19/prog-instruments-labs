import json
import sys


def read_json_file(filename: str) -> dict:
    """
    Читает JSON файл и возвращает словарь
    :param filename: Путь к JSON файлу
    :return: Данные из файла как словарь
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"JSON файл '{filename}' не найден.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка формата JSON в файле '{filename}'")
        sys.exit(1)


def read_file(filename: str) -> str:
    """
    Читает файл с последовательностью
    :param filename: Путь к файлу для чтения.
    :return: Последовательность
    """
    try:

        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка чтения файла '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла '{filename}': {e}")
        sys.exit(1)


def write_file(filename: str, text: str) -> None:
    """
    Записывает текст в файл
    :param filename: Путь к файлу
    :param content: Текст для записи
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except IOError as e:
        print(f"Ошибка записи в файл '{filename}': {e}")
        sys.exit(1)