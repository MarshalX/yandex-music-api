from typing import Dict

from yandex_music import Client, JSONType, SearchBanner


class TestSearchBanner:
    text = 'Слушайте новый альбом'
    text_for_search = 'новый альбом'
    url = 'https://music.yandex.ru/album/100500'
    url_scheme = 'yandexmusic://album/100500'
    text_color = '#FFFFFF'
    text_background_color = '#000000'
    image_url = 'avatars.yandex.net/get-music-misc/12345/banner/%%'

    def test_expected_values(self, search_banner: SearchBanner) -> None:
        assert search_banner.text == self.text
        assert search_banner.text_for_search == self.text_for_search
        assert search_banner.url == self.url
        assert search_banner.url_scheme == self.url_scheme
        assert search_banner.text_color == self.text_color
        assert search_banner.text_background_color == self.text_background_color
        assert search_banner.image_url == self.image_url

    def test_de_json_none(self, client: Client) -> None:
        assert SearchBanner.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'text': self.text,
            'textForSearch': self.text_for_search,
            'url': self.url,
            'urlScheme': self.url_scheme,
            'textColor': self.text_color,
            'textBackgroundColor': self.text_background_color,
            'imageUrl': self.image_url,
        }
        obj = SearchBanner.de_json(json_dict, client)
        assert obj is not None

        assert obj.text == self.text
        assert obj.text_for_search == self.text_for_search
        assert obj.url == self.url
        assert obj.url_scheme == self.url_scheme
        assert obj.text_color == self.text_color
        assert obj.text_background_color == self.text_background_color
        assert obj.image_url == self.image_url

    def test_equality(self) -> None:
        a = SearchBanner(text=self.text, url=self.url)
        b = SearchBanner(text=self.text, url='https://music.yandex.ru/album/1')
        c = SearchBanner(text=self.text, url=self.url)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
