from typing import Union
from dataclasses import dataclass
import datetime
import hmac
import hashlib
import base64

from yandex_music.utils.convert_track_id import convert_track_id_to_number


DEFAULT_SIGN_KEY = 'p93jhgh689SBReK6ghtw62'


@dataclass
class Sign:
    """TODO"""

    timestamp: int
    value: str


def get_sign_request(track_id: Union[int, str], key: str = DEFAULT_SIGN_KEY) -> Sign:
    """TODO"""
    track_id = convert_track_id_to_number(track_id)

    timestamp = int(datetime.datetime.now().timestamp())
    message = f'{track_id}{timestamp}'

    hmac_sign = hmac.new(key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).digest()
    sign = base64.b64encode(hmac_sign).decode('UTF-8')

    return Sign(timestamp, sign)
