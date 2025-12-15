# work_files.py
import json
import sys
from logging_config import get_module_logger

# Получаем логгер для этого модуля
logger = get_module_logger('work_files')


def read_json_file(filename: str) -> dict:
    """
    Читает JSON файл и возвращает словарь
    :param filename: Путь к JSON файлу
    :return: Данные из файла как словарь
    """
    try:
        logger.info(f"Начинаю чтение JSON файла: {filename}")
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"JSON файл '{filename}' успешно прочитан. Ключи: {list(data.keys())}")
            return data
    except FileNotFoundError:
        logger.error(f"JSON файл '{filename}' не найден.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка формата JSON в файле '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неизвестная ошибка при чтении JSON файла '{filename}': {e}")
        sys.exit(1)


def read_file(filename: str) -> str:
    """
    Читает файл с последовательностью
    :param filename: Путь к файлу для чтения.
    :return: Последовательность
    """
    try:
        logger.info(f"Начинаю чтение файла: {filename}")
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"Файл '{filename}' успешно прочитан. Длина: {len(content)} символов")
            return content
    except FileNotFoundError:
        logger.error(f"Файл '{filename}' не найден.")
        sys.exit(1)
    except IOError as e:
        logger.error(f"Ошибка чтения файла '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неизвестная ошибка при чтении файла '{filename}': {e}")
        sys.exit(1)


def write_file(filename: str, text: str) -> None:
    """
    Записывает текст в файл
    :param filename: Путь к файлу
    :param content: Текст для записи
    """
    try:
        logger.info(f"Начинаю запись в файл: {filename}")
        logger.debug(f"Длина записываемого текста: {len(text)} символов")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logger.info(f"Файл '{filename}' успешно записан")
    except IOError as e:
        logger.error(f"Ошибка записи в файл '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неизвестная ошибка при записи файла '{filename}': {e}")
        sys.exit(1)