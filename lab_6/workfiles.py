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


def write_json_file(filename: str, data: dict) -> None:
    """
    Записывает данные в JSON файл
    :param filename: Путь к файлу
    :param data: Данные для записи
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        print(f"JSON файл '{filename}' не найден.")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка записи JSON в файл '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка при записи в файл '{filename}': {e}")
        sys.exit(1)


def read_text_file(filename: str) -> str:
    """
    Читает содержимое текстового файла
    :param filename: Путь к файлу
    :return: Содержимое файла как строка
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


def write_text_file(filename: str, content: str) -> None:
    """
    Записывает текст в файл
    :param filename: Путь к файлу
    :param content: Текст для записи
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        print(f"Ошибка записи в файл '{filename}': {e}")
        sys.exit(1)


def read_key_from_json(filename: str) -> str:
    """
    Читает ключ из JSON файла
    :param filename: Путь к JSON файлу с ключом
    :return: Ключ шифрования
    """
    data = read_json_file(filename)
    if not isinstance(data, str):
        raise ValueError("Ключ должен быть строкой")
    return data