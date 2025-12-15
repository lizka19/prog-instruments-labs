import sys
import math
from logging_config import get_module_logger
from work_files import read_json_file, read_file, write_file
from scipy.special import gammainc

# Получаем логгер для этого модуля
logger = get_module_logger('tests')


def frequency_bit_test(sequence: str) -> float:
    """
    Выполняет тест на частоту битов.
    :param sequence: Битовая последовательность
    :return: P-значение
    """
    try:
        n = len(sequence)
        logger.info(f"Тест частоты битов: длина последовательности = {n}")

        if n == 0:
            logger.error("Последовательность пуста")
            raise ValueError("Sequence is empty")

        # Вычисляем сумму битов
        s = sum([1 if bit == "1" else -1 for bit in sequence])
        logger.debug(f"Сумма битов (S_n) = {s}")

        # Вычисляем p-значение
        p_value = math.erfc((abs(s) / math.sqrt(n)) / math.sqrt(2))
        logger.info(f"Тест частоты битов завершен. P-значение = {p_value:.6f}")

        return p_value
    except Exception as e:
        logger.error(f"Ошибка в тесте частоты битов: {e}")
        raise


def same_bits_test(sequence: str) -> float:
    """
    Выполняет тест на идентичные последовательные биты.
    :param sequence: Последовательность
    :return: P-значение
    """
    try:
        logger.info(f"Тест идентичных последовательных битов: длина = {len(sequence)}")
        n = len(sequence)

        # Вычисляем вероятность появления '1'
        p = sequence.count('1') / n
        logger.debug(f"Вероятность появления '1' = {p:.4f}")

        # Проверяем условие
        if abs(p - 0.5) >= 2 / math.sqrt(n):
            logger.warning(f"Вероятность {p:.4f} выходит за допустимые пределы, возвращаем 0")
            return 0.0

        # Подсчитываем изменения битов
        v_n = 0
        for i in range(n - 1):
            if sequence[i] != sequence[i + 1]:
                v_n += 1

        logger.debug(f"Количество изменений (V_n) = {v_n}")

        # Вычисляем p-значение
        numerator = abs(v_n - 2 * n * p * (1 - p))
        denominator = 2 * math.sqrt(2 * n) * p * (1 - p)
        p_value = math.erfc(numerator / denominator)

        logger.info(f"Тест идентичных битов завершен. P-значение = {p_value:.6f}")
        return p_value
    except Exception as e:
        logger.error(f"Ошибка в тесте идентичных битов: {e}")
        raise


def longest_sequence_test(sequence: str, PI: list, block_size: int = 8) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц в блоке.
    """
    try:
        n = len(sequence)
        logger.info(f"Тест самой длинной последовательности: длина = {n}, размер блока = {block_size}")

        if n < 128:
            logger.error(f"Недостаточная длина последовательности: {n} < 128")
            raise ValueError("Minimum 128 bits")

        N = n // block_size
        v = [0] * (max(4, (block_size + 1) // 2))

        logger.debug(f"Количество блоков N = {N}")
        logger.debug(f"Размер массива v = {len(v)}")

        # Анализируем каждый блок
        for i in range(N):
            block = sequence[i * block_size: (i + 1) * block_size]
            max_run = 0
            current_run = 0

            for bit in block:
                if bit == '1':
                    current_run += 1
                    if current_run > max_run:
                        max_run = current_run
                else:
                    current_run = 0

            if max_run < len(v):
                v[max_run] += 1
            else:
                v[-1] += 1

        logger.debug(f"Распределение длин последовательностей: {v}")

        # Вычисляем хи-квадрат статистику
        x_2 = 0.0
        for i in range(len(v)):
            if PI[i] > 0:
                expected = N * PI[i]
                observed = v[i]
                contribution = (observed - expected) ** 2 / expected
                x_2 += contribution
                logger.debug(
                    f"Индекс {i}: ожидаемо = {expected:.2f}, наблюдаемо = {observed}, вклад = {contribution:.4f}")

        logger.debug(f"Статистика хи-квадрат = {x_2:.4f}")

        # Вычисляем p-значение
        p_value = gammainc(len(v) / 2, x_2 / 2)
        logger.info(f"Тест самой длинной последовательности завершен. P-значение = {p_value:.6f}")

        return p_value
    except Exception as e:
        logger.error(f"Ошибка в тесте самой длинной последовательности: {e}")
        raise


def main():
    """
    Основная функция для запуска тестов
    """
    try:
        logger.info("---")
        logger.info("НАЧАЛО ВЫПОЛНЕНИЯ СТАТИСТИЧЕСКИХ ТЕСТОВ")
        logger.info("---")

        # Загрузка конфигурации
        logger.info("Загрузка конфигурации...")
        config = read_json_file('consts.json')
        logger.info("Конфигурация успешно загружена")

        # Извлечение параметров из конфигурации
        cpp_sequence_txt = config["cpp_sequence_txt"]
        java_sequence_txt = config["java_sequence_txt"]
        test_results_cpp = config["test_results_cpp"]
        test_results_java = config["test_results_java"]
        PI = config["PI"]

        logger.info(f"Файл C++ последовательности: {cpp_sequence_txt}")
        logger.info(f"Файл Java последовательности: {java_sequence_txt}")
        logger.info(f"Вероятности PI: {PI}")

        # Тестирование C++ последовательности
        logger.info("---")
        logger.info("ТЕСТИРОВАНИЕ C++ ПОСЛЕДОВАТЕЛЬНОСТИ")
        logger.info("---")

        cpp_sequence = read_file(cpp_sequence_txt)
        logger.info(f"C++ последовательность загружена, длина = {len(cpp_sequence)}")

        # Выполнение тестов для C++
        p_val_freq_bits_cpp = frequency_bit_test(cpp_sequence)
        p_val_ident_bits_cpp = same_bits_test(cpp_sequence)
        p_val_longest_bits_block_cpp = longest_sequence_test(cpp_sequence, PI)

        # Формирование результатов
        result_cpp_test = (f"CPP sequence: {cpp_sequence}\n\n"
                           f"Frequency bit test: {p_val_freq_bits_cpp}\n"
                           f"Test for identical consecutive bits: {p_val_ident_bits_cpp}\n"
                           f"Test for the longest sequence of ones in a block: "
                           f"{p_val_longest_bits_block_cpp}")

        logger.info(f"C++ тесты завершены. Сохраняю результаты в {test_results_cpp}")
        write_file(test_results_cpp, result_cpp_test)

        # Тестирование Java последовательности
        logger.info("---")
        logger.info("ТЕСТИРОВАНИЕ JAVA ПОСЛЕДОВАТЕЛЬНОСТИ")
        logger.info("---")

        java_sequence = read_file(java_sequence_txt)
        logger.info(f"Java последовательность загружена, длина = {len(java_sequence)}")

        # Выполнение тестов для Java
        p_val_freq_bits_java = frequency_bit_test(java_sequence)
        p_val_ident_bits_java = same_bits_test(java_sequence)
        p_val_longest_bits_block_java = longest_sequence_test(java_sequence, PI)

        # Формирование результатов
        result_java_test = (f"Java sequence: {java_sequence}\n\n"
                            f"Frequency bit test: {p_val_freq_bits_java}\n"
                            f"Test for identical consecutive bits: {p_val_ident_bits_java}\n"
                            f"Test for the longest sequence of ones in a block: "
                            f"{p_val_longest_bits_block_java}")

        logger.info(f"Java тесты завершены. Сохраняю результаты в {test_results_java}")
        write_file(test_results_java, result_java_test)

        # Сводка результатов
        logger.info("---")
        logger.info("СВОДКА РЕЗУЛЬТАТОВ")
        logger.info("---")
        logger.info(f"C++ последовательность:")
        logger.info(f"  - Тест частоты битов: {p_val_freq_bits_cpp:.6f}")
        logger.info(f"  - Тест идентичных битов: {p_val_ident_bits_cpp:.6f}")
        logger.info(f"  - Тест длинной последовательности: {p_val_longest_bits_block_cpp:.6f}")
        logger.info(f"Java последовательность:")
        logger.info(f"  - Тест частоты битов: {p_val_freq_bits_java:.6f}")
        logger.info(f"  - Тест идентичных битов: {p_val_ident_bits_java:.6f}")
        logger.info(f"  - Тест длинной последовательности: {p_val_longest_bits_block_java:.6f}")
        logger.info("---")
        logger.info("ВСЕ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ")
        logger.info("---")

    except Exception as e:
        logger.error(f"Критическая ошибка в основной программе: {e}")
        logger.exception("Детали исключения:")
        raise


if __name__ == "__main__":
    # Инициализация логирования
    from logging_config import setup_logging

    setup_logging()

    main()