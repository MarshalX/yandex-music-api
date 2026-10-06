from typing import Dict, Optional

from yandex_music import Client, Cover, CoverDerivedColors, Images, JSONType


class TestCover:
    type = 'pic'
    uri = 'avatars.yandex.net/get-music-user-playlist/38125/q0ahkhfQE3neTk/%%?1572609906461'
    items_uri = [
        'avatars.yandex.net/get-music-user-playlist/38125/q0ahkhfQE3neTk/%%?1572609906461',
        'avatars.yandex.net/get-music-user-playlist/38125/q0ahkhfQE3neTk/%%?1572609906461',
    ]
    dir = '/get-music-user-playlist/34120/pvg900XixWaHcr/'
    version = '1572609906461'
    custom = True
    is_custom = True
    prefix: Optional[str] = None
    copyright_name = 'ТАСС'
    copyright_cline = 'imago stock&people'
    error: Optional[str] = None
    color = '#6d6e72'

    def test_expected_values(self, cover: Cover, cover_derived_colors: CoverDerivedColors) -> None:
        assert cover.type == self.type
        assert cover.uri == self.uri
        assert cover.items_uri == self.items_uri
        assert cover.dir == self.dir
        assert cover.version == self.version
        assert cover.custom == self.custom
        assert cover.is_custom == self.is_custom
        assert cover.copyright_name == self.copyright_name
        assert cover.copyright_cline == self.copyright_cline
        assert cover.prefix == self.prefix
        assert cover.error == self.error
        assert cover.color == self.color
        assert cover.derived_colors == cover_derived_colors

    def test_de_json_none(self, client: Client) -> None:
        assert Cover.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Cover.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {}
        _ = Cover.de_json(json_dict, client)

    def test_de_json_all(self, client: Client, cover_derived_colors: CoverDerivedColors) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'uri': self.uri,
            'items_uri': self.items_uri,
            'dir': self.dir,
            'version': self.version,
            'custom': self.custom,
            'is_custom': self.is_custom,
            'prefix': self.prefix,
            'error': self.error,
            'copyright_name': self.copyright_name,
            'copyright_cline': self.copyright_cline,
            'color': self.color,
            'derivedColors': cover_derived_colors.to_dict(),
        }
        cover = Cover.de_json(json_dict, client)
        assert cover is not None

        assert cover.type == self.type
        assert cover.uri == self.uri
        assert cover.items_uri == self.items_uri
        assert cover.dir == self.dir
        assert cover.version == self.version
        assert cover.custom == self.custom
        assert cover.is_custom == self.is_custom
        assert cover.copyright_name == self.copyright_name
        assert cover.copyright_cline == self.copyright_cline
        assert cover.prefix == self.prefix
        assert cover.error == self.error
        assert cover.color == self.color
        assert cover.derived_colors == cover_derived_colors

    def test_equality(self, images: Images) -> None:
        a = Cover(self.type, self.uri, self.items_uri)

        assert a != images
        assert hash(a) != hash(images)
        assert a is not images
