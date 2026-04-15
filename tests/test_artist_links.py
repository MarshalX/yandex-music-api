from yandex_music import ArtistLinks


class TestArtistLinks:
    def test_expected_value(self, artist_links_fixture, artist_link):
        assert artist_links_fixture.links == [artist_link]

    def test_de_json_none(self, client):
        assert ArtistLinks.de_json({}, client) is None

    def test_de_json_all(self, client, artist_link):
        json_dict = {
            'links': [artist_link.to_dict()],
        }
        artist_links = ArtistLinks.de_json(json_dict, client)

        assert artist_links.links == [artist_link]

    def test_equality(self, artist_link):
        a = ArtistLinks(links=[artist_link])
        b = ArtistLinks(links=None)
        c = ArtistLinks(links=[artist_link])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
