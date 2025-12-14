import argparse
import sys

sys.path.append(r'C:\Users\lizak\PycharmProjects\prog-instruments-labs\lab_6')

from argparse import Namespace
from workfiles import read_key_from_json, read_text_file, write_text_file
from vigenere import vigenere_cipher_encrypt


def parser() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_text', type=str, help='Имя файла с исходным текстом')
    parser.add_argument('output_text', type=str, help='Имя файла для сохранения результата')
    parser.add_argument('key', type=str, help='JSON-файл с ключом шифрования')
    return parser.parse_args()


def main():
    args = parser()

    key = read_key_from_json(args.key)

    input_text = read_text_file(args.input_text)
    encrypted_text = vigenere_cipher_encrypt(input_text, key)

    write_text_file(args.output_text, encrypted_text)

if __name__ == "__main__":
    main()