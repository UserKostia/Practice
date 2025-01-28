import os
import hashlib


def verify_password(password: str, hashed_password: str) -> bool:
    """Перевіряє відповідність пароля його хешу."""
    # Розділяємо сіль і хеш
    salt_hex, hashed = hashed_password.split(':')
    salt = bytes.fromhex(salt_hex)  # Перетворюємо сіль з шістнадцяткового рядка в байти
    # Хешуємо введений пароль з тією ж сіллю
    new_hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    # Порівнюємо новий хеш з оригінальним
    return new_hashed.hex() == hashed


def get_password_hash(password: str) -> str:
    """Генерує хеш пароля за допомогою hashlib."""
    # Генерація випадкової солі
    salt = os.urandom(16)  # 16 байт
    # Хешування пароля з сіллю
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',  # Алгоритм хешування
        password.encode('utf-8'),  # Перетворення пароля в байти
        salt,  # Сіль
        100000  # Кількість ітерацій
    )
    # Повертаємо сіль і хеш у вигляді шістнадцяткового рядка
    return salt.hex() + ':' + hashed_password.hex()
