from yandex_music import ArtistLink


class TestArtistLink:
    title = 'Official Site'
    subtitle = 'example.com'
    url = 'https://example.com'
    img_url = 'avatars.yandex.net/get-music-misc/12345/img.abc123/%%'

    def test_expected_values(self, artist_link):
        assert artist_link.title == self.title
        assert artist_link.subtitle == self.subtitle
        assert artist_link.url == self.url
        assert artist_link.img_url == self.img_url

    def test_de_json_none(self, client):
        assert ArtistLink.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'subtitle': self.subtitle,
            'url': self.url,
            'img_url': self.img_url,
        }
        artist_link = ArtistLink.de_json(json_dict, client)

        assert artist_link.title == self.title
        assert artist_link.subtitle == self.subtitle
        assert artist_link.url == self.url
        assert artist_link.img_url == self.img_url

    def test_de_list_none(self, client):
        assert ArtistLink.de_list([], client) == []

    def test_equality(self):
        a = ArtistLink(self.title, self.subtitle, self.url, self.img_url)
        b = ArtistLink(self.title, self.subtitle, '', self.img_url)
        c = ArtistLink('', self.subtitle, self.url, self.img_url)
        d = ArtistLink(self.title, self.subtitle, self.url, self.img_url)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
