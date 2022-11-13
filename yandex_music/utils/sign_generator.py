from typing import NamedTuple
from datetime import datetime
import hmac
import hashlib
import base64


class Sign(NamedTuple):
    timestamp: int
    sign: str


class SignGenerator:
    def __init__(self,
                 track_id: int,
                 secret: str = 'p93jhgh689SBReK6ghtw62'):
        self.track_id = track_id
        self.secret = secret

    def get_sign(self) -> str:
        timestamp = int(datetime.now().timestamp())
        message = f'{self.track_id}{timestamp}'

        hmac_sign = hmac.new(self.secret.encode('UTF-8'),
                             message.encode('UTF-8'), hashlib.sha256).digest()
        sign = base64.b64encode(hmac_sign).decode('UTF-8')

        return Sign(
            timestamp=timestamp,
            sign=sign
        )
