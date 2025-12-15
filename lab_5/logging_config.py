# logging_config.py
import logging
import sys


def setup_logging():
    """
    Настройка системы логирования для всего проекта
    """
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем обработчик для файла
    file_handler = logging.FileHandler('project.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Создаем обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)  # В консоль только ошибки

    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Отключаем логирование для некоторых библиотек
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    return root_logger


# Создаем отдельные логгеры для разных модулей
def get_module_logger(module_name):
    """
    Получить логгер для конкретного модуля
    """
    logger = logging.getLogger(module_name)
    return logger


# Инициализация при импорте
logger = get_module_logger('main')