import sys
sys.path.append(r'C:\Users\lizak\PycharmProjects\prog-instruments-labs\lab_5')
import math

from work_files import *
from scipy.special import gammainc


def frequency_bit_test(sequence: str) -> float:
    """
    Выполняет тест на частоту битов.
    :param sequence: Битовая последовательность
    :return: P-значение
    """
    n = len(sequence)

    if n == 0:
        raise ValueError("Sequence is empty")

    s = sum([1 if bit == "1" else -1 for bit in sequence])

    p_value = math.erfc((abs(s) / math.sqrt(n)) / math.sqrt(2))

    return p_value


def same_bits_test(sequence: str) -> float:
    """
    Выполняет тест на идентичные последовательные биты.
    :param sequence: Последовательность
    :return: P-значение
    """
    p_value = 0

    n = len(sequence)

    p = sequence.count('1') / n

    if abs(p - 0.5) >= 2 / math.sqrt(n):
        return p_value

    v_n = 0

    for i in range(n - 1):

        if sequence[i] != sequence[i + 1]:
            v_n += 1

    numerator = abs(v_n - 2 * n * p * (1 - p))
    denominator = 2 * math.sqrt(2 * n) * p * (1 - p)

    return math.erfc(numerator / denominator)

def longest_sequence_test(sequence: str, PI: list, block_size: int = 8) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц в блоке.
    :param sequence: Последовательность
    :param PI: Ожидаемые вероятности для различных длин последовательностей
    :param block_size: Размер блока (по умолчанию 8)
    :return: P-значение
    """

    n = len(sequence)

    if n < 128:
        raise ValueError("Minimum 128 bits")

    N = n // block_size
    v = [0] * (max(4, (block_size + 1) // 2))

    for i in range(N):
        block = sequence[i * block_size : (i + 1) * block_size]

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

    x_2 = 0.0

    for i in range(len(v)):
        x_2 += (v[i] - (N * PI[i])) ** 2 / (N * PI[i]) if PI[i] > 0 else 0

    p_value = gammainc(len(v) / 2, x_2 / 2)
    return p_value

def main():
    try:
        config = read_json_file('consts.json')

        cpp_sequence_txt = config["cpp_sequence_txt"]
        java_sequence_txt = config["java_sequence_txt"]
        test_results_cpp = config["test_results_cpp"]
        test_results_java = config["test_results_java"]
        PI = config["PI"]

        cpp_sequence = read_file(cpp_sequence_txt)
        java_sequence = read_file(java_sequence_txt)

        p_val_freq_bits_cpp = frequency_bit_test(cpp_sequence)
        p_val_ident_bits_cpp = same_bits_test(cpp_sequence)
        p_val_longest_bits_block_cpp = longest_sequence_test(cpp_sequence, PI)

        result_cpp_test = (f"CPP sequence: {cpp_sequence}\n\n"
                           f"Frequency bit test: {p_val_freq_bits_cpp}\n"
                           f"Test for identical consecutive bits: {p_val_ident_bits_cpp}\n"
                           f"Test for the longest sequence of ones in a block: "
                           f"{p_val_longest_bits_block_cpp}")

        write_file(test_results_cpp, result_cpp_test)

        p_val_freq_bits_java = frequency_bit_test(java_sequence)
        p_val_ident_bits_java = same_bits_test(java_sequence)
        p_val_longest_bits_block_java = longest_sequence_test(java_sequence, PI)

        result_java_test = (f"Java sequence: {java_sequence}\n\n"
                            f"Frequency bit test: {p_val_freq_bits_java}\n"
                            f"Test for identical consecutive bits: {p_val_ident_bits_java}\n"
                            f"Test for the longest sequence of ones in a block: "
                            f"{p_val_longest_bits_block_java}")

        write_file(test_results_java, result_java_test)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
