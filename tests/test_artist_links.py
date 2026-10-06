from typing import Dict

from yandex_music import ArtistLink, ArtistLinks, Client, JSONType


class TestArtistLinks:
    def test_expected_value(self, artist_links_fixture: ArtistLinks, artist_link: ArtistLink) -> None:
        assert artist_links_fixture.links == [artist_link]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistLinks.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist_link: ArtistLink) -> None:
        json_dict: Dict[str, JSONType] = {
            'links': [artist_link.to_dict()],
        }
        artist_links = ArtistLinks.de_json(json_dict, client)
        assert artist_links is not None

        assert artist_links.links == [artist_link]

    def test_equality(self, artist_link: ArtistLink) -> None:
        a = ArtistLinks(links=[artist_link])
        b = ArtistLinks(links=None)
        c = ArtistLinks(links=[artist_link])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
