from workfiles import read_json_file


def get_alphabet():
    """
    Получает алфавит из файла с константами
    """
    return read_json_file('const.json')['ALPHABET']

def is_valid_char(char: str) -> bool:
    """
    Проверяет, является ли символ допустимым (содержится в алфавите).
    :param char: Символ для проверки.
    :return: True, если символ допустим, иначе False.
    """
    return char.lower() in get_alphabet()


def get_key_symbol(key: str, index: int) -> str:
    """
    Получает символ ключа по индексу, используя циклический доступ.
    :param key: Ключ шифрования.
    :param index: Индекс символа в тексте.
    :return: Символ ключа, соответствующий индексу.
    :raises ValueError: Если ключ пустой.
    """
    if not key:
        raise ValueError("Key can't be empty!")
    return key[index % len(key)]


def get_encrypted_symbol(old_symbol: str, key_symbol: str) -> str:
    """
    Шифрует символ, используя символ ключа.
    :param old_symbol: Символ, который нужно зашифровать.
    :param key_symbol: Символ ключа для шифрования.
    :return: Зашифрованный символ или оригинальный, если он не является буквой.
    """
    alphabet = get_alphabet()

    if not is_valid_char(old_symbol) or not is_valid_char(key_symbol):
        return old_symbol

    try:
        current_idx = alphabet.index(old_symbol.lower())
        key_idx = alphabet.index(key_symbol.lower())
    except ValueError:
        return old_symbol

    encrypt_idx = (current_idx + key_idx) % len(alphabet)

    # ВОЗВРАЩАЕМ СИМВОЛ С СОХРАНЕНИЕМ РЕГИСТРА
    if old_symbol.isupper():
        return alphabet[encrypt_idx].upper()
    else:
        return alphabet[encrypt_idx]
def vigenere_cipher_encrypt(input_text: str, key: str) -> str:
    """
    Шифрует текст с использованием шифра Виженера.
    :param input_text: Текст для шифрования.
    :param key: Ключ шифрования.
    :return: Зашифрованный текст.
    :raises ValueError: Если входной текст или ключ пусты.
    """
    if not input_text:
        raise ValueError("Input text can't be empty")
    if not key:
        raise ValueError("Key can't be empty")

    clean_key = ''.join(c for c in key if is_valid_char(c))
    if not clean_key:
        raise ValueError("Key must contain at least one valid character from the alphabet")

    encrypted_text = []
    for i in range(len(input_text)):
        text_symbol = input_text[i]
        key_symbol = get_key_symbol(clean_key, i)
        encrypted_text.append(get_encrypted_symbol(text_symbol, key_symbol))

    return ''.join(encrypted_text)


def get_decrypted_symbol(encrypted_symbol: str, key_sym: str) -> str:
    """
    Дешифрует символ, используя символ ключа.
    :param encrypted_symbol: Зашифрованный символ.
    :param key_sym: Символ ключа для дешифрования.
    :return: Дешифрованный символ или оригинальный, если он не является буквой.
    """
    alphabet = get_alphabet()

    if not is_valid_char(encrypted_symbol) or not is_valid_char(key_sym):
        return encrypted_symbol

    try:
        encrypted_idx = alphabet.index(encrypted_symbol.lower())
        key_idx = alphabet.index(key_sym.lower())
    except ValueError:
        return encrypted_symbol

    decrypted_idx = (encrypted_idx - key_idx) % len(alphabet)
    if encrypted_symbol.isupper():
        return alphabet[decrypted_idx].upper()
    else:
        return alphabet[decrypted_idx]
def vigenere_cipher_decrypt(encrypted_text: str, key: str) -> str:
    """
    Дешифрует текст, зашифрованный с использованием шифра Виженера.
    :param encrypted_text: Зашифрованный текст для дешифрования.
    :param key: Ключ шифрования.
    :return: Дешифрованный текст.
    :raises ValueError: Если зашифрованный текст или ключ пусты.
    """
    if not encrypted_text:
        raise ValueError("Encrypted text can't be empty")
    if not key:
        raise ValueError("Key can't be empty")

    clean_key = ''.join(c for c in key if is_valid_char(c))
    if not clean_key:
        raise ValueError("Key must contain at least one valid character from the alphabet")

    decrypted_text = []
    for i in range(len(encrypted_text)):
        encrypted_symbol = encrypted_text[i]
        key_symbol = get_key_symbol(clean_key, i)
        decrypted_text.append(get_decrypted_symbol(encrypted_symbol, key_symbol))

    return ''.join(decrypted_text)