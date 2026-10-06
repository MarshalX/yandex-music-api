from typing import Dict, List, Optional

import pytest

from yandex_music import Client, Genre, Icon, Images, JSONType, Title


@pytest.fixture(scope='class')
def genre(title: Title, images: Images, icon: Icon, genre_without_sub_genre: Genre) -> Genre:
    return Genre(
        TestGenre.id,
        TestGenre.weight,
        TestGenre.composer_top,
        TestGenre.title,
        {'uz': title},
        images,
        TestGenre.show_in_menu,
        TestGenre.show_in_regions,
        TestGenre.full_title,
        TestGenre.url_part,
        TestGenre.color,
        icon,
        [genre_without_sub_genre],
        TestGenre.hide_in_regions,
    )


@pytest.fixture(scope='class')
def genre_without_sub_genre(title: Title, images: Images, icon: Icon) -> Genre:
    return Genre(
        TestGenre.id,
        TestGenre.weight,
        TestGenre.composer_top,
        TestGenre.title,
        {'uz': title},
        images,
        TestGenre.show_in_menu,
    )


class TestGenre:
    id = 'all'
    weight = 2
    composer_top = False
    title = 'Все жанры'
    show_in_menu = True
    show_in_regions = [181]
    full_title = 'Музыка всех жанров'
    url_part: Optional[str] = None
    color: Optional[str] = None
    hide_in_regions: Optional[List[int]] = None

    def test_expected_values(
        self, genre: Genre, title: Title, images: Images, icon: Icon, genre_without_sub_genre: Genre
    ) -> None:
        assert genre.id == self.id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == {'uz': title}
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu
        assert genre.show_in_regions == self.show_in_regions
        assert genre.full_title == self.full_title
        assert genre.url_part == self.url_part
        assert genre.color == self.color
        assert genre.radio_icon == icon
        assert genre.sub_genres == [genre_without_sub_genre]
        assert genre.hide_in_regions == self.hide_in_regions

    def test_de_json_none(self, client: Client) -> None:
        assert Genre.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Genre.de_list([], client) == []

    def test_de_json_required(self, client: Client, title: Title, images: Images) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'weight': self.weight,
            'composer_top': self.composer_top,
            'title': self.title,
            'titles': {'uz': title.to_dict()},
            'images': images.to_dict(),
            'show_in_menu': self.show_in_menu,
        }
        genre = Genre.de_json(json_dict, client)
        assert genre is not None

        assert genre.id == self.id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == {'uz': title}
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu

    def test_de_json_all(
        self, client: Client, title: Title, images: Images, icon: Icon, genre_without_sub_genre: Genre
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'weight': self.weight,
            'composer_top': self.composer_top,
            'title': self.title,
            'titles': {'uz': title.to_dict()},
            'images': images.to_dict(),
            'show_in_menu': self.show_in_menu,
            'full_title': self.full_title,
            'url_part': self.url_part,
            'color': self.color,
            'radio_icon': icon.to_dict(),
            'sub_genres': [genre_without_sub_genre.to_dict()],
            'hide_in_regions': self.hide_in_regions,
            'show_in_regions': self.show_in_regions,
        }
        genre = Genre.de_json(json_dict, client)
        assert genre is not None

        assert genre.id == self.id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == {'uz': title}
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu
        assert genre.show_in_regions == self.show_in_regions
        assert genre.full_title == self.full_title
        assert genre.url_part == self.url_part
        assert genre.color == self.color
        assert genre.radio_icon == icon
        assert genre.sub_genres == [genre_without_sub_genre]
        assert genre.hide_in_regions == self.hide_in_regions

    def test_equality(self, title: Title, images: Images) -> None:
        a = Genre(self.id, self.weight, self.composer_top, self.title, {'uz': title}, images, self.show_in_menu)
        b = Genre(self.id, self.weight, False, '', {'uz': title}, images, self.show_in_menu)
        c = Genre(self.id, 30, self.composer_top, self.title, {'uz': title}, images, self.show_in_menu)
        d = Genre(self.id, self.weight, self.composer_top, self.title, {'uz': title}, images, self.show_in_menu)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
