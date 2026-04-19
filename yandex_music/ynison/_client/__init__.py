"""Внутренняя реализация клиентов Ynison."""

from yandex_music.ynison._client.client import YnisonClient
from yandex_music.ynison._client.client_async import YnisonClientAsync

__all__ = ['YnisonClient', 'YnisonClientAsync']
