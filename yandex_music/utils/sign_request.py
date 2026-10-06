"""Подпись HTTP-запросов."""

import base64
import datetime
import hashlib
import hmac
from dataclasses import dataclass
from typing import List, Union

from yandex_music.utils.convert_track_id import convert_track_id_to_number

DEFAULT_SIGN_KEY = 'p93jhgh689SBReK6ghtw62'
""":obj:`str`: Ключ для подписи из Android приложения."""

DESKTOP_SIGN_KEY = 'kzqU4XhfCaY6B6JTHODeq5'
""":obj:`str`: Ключ для подписи из десктопного приложения для Windows."""

DESKTOP_CLIENT = 'YandexMusicDesktopAppWindows/5.95.0'
""":obj:`str`: Значение заголовка `X-Yandex-Music-Client`, к которому привязан :attr:`DESKTOP_SIGN_KEY`."""


@dataclass
class Sign:
    """Подпись запроса.

    Attributes:
        timestamp (:obj:`int`): Время создания подписи.
        value (:obj:`str`): Подпись.
    """

    timestamp: int
    value: str


def get_sign_request(track_id: Union[int, str], key: str = DEFAULT_SIGN_KEY) -> Sign:
    """Создает подпись для запроса.

    Args:
        track_id (:obj:`str` | :obj:`int`): Уникальный идентификатора трека.
        key (:obj:`str`, optional): Ключ для подписи.

    Returns:
        :obj:`Sign`: Подпись.
    """
    track_id = convert_track_id_to_number(track_id)

    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    message = f'{track_id}{timestamp}'

    hmac_sign = hmac.new(key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).digest()
    sign = base64.b64encode(hmac_sign).decode('UTF-8')

    return Sign(timestamp, sign)


def get_file_info_sign(
    track_id: Union[int, str],
    quality: str,
    codecs: List[str],
    transport: str,
    key: str = DESKTOP_SIGN_KEY,
) -> Sign:
    """Создает подпись для запроса информации о файле трека.

    Note:
        Подпись проверяется вместе с заголовком `X-Yandex-Music-Client`, соответствующим ключу.

    Args:
        track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека в том же виде, что и в запросе.
        quality (:obj:`str`): Качество.
        codecs (:obj:`list` из :obj:`str`): Кодеки.
        transport (:obj:`str`): Способ доставки файла.
        key (:obj:`str`, optional): Ключ для подписи.

    Returns:
        :obj:`Sign`: Подпись.
    """
    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    message = f'{timestamp}{track_id}{quality}{"".join(codecs)}{transport}'

    hmac_sign = hmac.new(key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).digest()
    sign = base64.b64encode(hmac_sign).decode('UTF-8')[:-1]

    return Sign(timestamp, sign)
