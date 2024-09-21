from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, LyricsMajor


@model
class TrackLyrics(YandexMusicModel):
    """Класс, представляющий текст трека.

    Attributes:
        download_url (:obj:`str`): Ссылка на скачивание текста.
        lyric_id (:obj:`int`): Уникальный идентификатор текста.
        external_lyric_id (:obj:`str`): Уникальный идентификатор текста на сервисе предоставляющий текст.
        writers (:obj:`list` из :obj:`str`): Авторы текста.
        major (:obj:`yandex_music.LyricsMajor`): Сервис, откуда был получен текст.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    download_url: str
    lyric_id: int
    external_lyric_id: str
    writers: List[str]
    major: 'LyricsMajor'
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.lyric_id,
            self.external_lyric_id,
        )

    def fetch_lyrics(self) -> str:
        """Получает текст песни по ссылке :attr:`yandex_music.TrackLyrics.download_url`.

        Returns:
            :obj:`str`: Текст песни.
        """
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self.download_url).decode('UTF-8')

    async def fetch_lyrics_async(self) -> str:
        """Получает текст песни по ссылке :attr:`yandex_music.TrackLyrics.download_url`.

        Returns:
            :obj:`str`: Текст песни.
        """
        assert self.valid_async_client(self.client)
        return (await self.client.request.retrieve(self.download_url)).decode('UTF-8')

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackLyrics']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackLyrics`: Текст трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import LyricsMajor

        cls_data['major'] = LyricsMajor.de_json(data.get('major'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`fetch_lyrics`
    fetchLyrics = fetch_lyrics
    #: Псевдоним для :attr:`fetch_lyrics_async`
    fetchLyricsAsync = fetch_lyrics_async
