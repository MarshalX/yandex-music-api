"""Расшифровка аудиофайлов."""

from yandex_music.exceptions import YandexMusicError


def decrypt_track(data: bytes, key: str) -> bytes:
    """Расшифровывает аудиофайл, полученный со способом доставки `encraw`.

    Note:
        Используется AES-128 в режиме CTR с нулевым начальным значением счётчика.

        Требуется пакет `cryptography`: ``pip install "yandex-music[crypto]"``.

    Args:
        data (:obj:`bytes`): Зашифрованное содержимое файла.
        key (:obj:`str`): Ключ в шестнадцатеричном виде из :attr:`yandex_music.FileDownloadInfo.key`.

    Returns:
        :obj:`bytes`: Расшифрованное содержимое файла.

    Raises:
        :class:`yandex_music.exceptions.YandexMusicError`: Если не установлен пакет `cryptography`.
    """
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except ImportError as e:
        raise YandexMusicError('Decryption requires cryptography: pip install "yandex-music[crypto]"') from e

    decryptor = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CTR(bytes(16))).decryptor()
    return decryptor.update(data) + decryptor.finalize()
