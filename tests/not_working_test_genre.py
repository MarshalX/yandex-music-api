import pytest

from yandex_music import Genre


@pytest.fixture(scope='class')
def genre(titles, images, radio_icon, sub_genres):
    return Genre(TestGenre.id, TestGenre.weight, TestGenre.composer_top, TestGenre.title, titles, images,
                 TestGenre.show_in_menu, TestGenre.full_title, TestGenre.url_part, TestGenre.color, radio_icon,
                 sub_genres, TestGenre.hide_in_regions)


class TestGenre:
    weight = None
    composer_top = None
    title = None
    titles = None
    show_in_menu = None
    full_title = None
    url_part = None
    color = None
    hide_in_regions = None

    def test_expected_values(self, genre, id, images, radio_icon, sub_genres):
        assert genre.id == id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == self.titles
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu
        assert genre.full_title == self.full_title
        assert genre.url_part == self.url_part
        assert genre.color == self.color
        assert genre.radio_icon == radio_icon
        assert genre.sub_genres == sub_genres
        assert genre.hide_in_regions == self.hide_in_regions

    def test_de_json_required(self, client, id, images):
        json_dict = {'id': id, 'weight': self.weight, 'composer_top': self.composer_top, 'title': self.title,
                     'titles': self.titles, 'images': images, 'show_in_menu': self.show_in_menu}
        genre = Genre.de_json(json_dict, client)

        assert genre.id == id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == self.titles
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu

    def test_de_json_all(self, client, id, images, radio_icon, sub_genres):
        json_dict = {'id': id, 'weight': self.weight, 'composer_top': self.composer_top, 'title': self.title,
                     'titles': self.titles, 'images': images, 'show_in_menu': self.show_in_menu,
                     'full_title': self.full_title, 'url_part': self.url_part, 'color': self.color,
                     'radio_icon': radio_icon, 'sub_genres': sub_genres, 'hide_in_regions': self.hide_in_regions}
        genre = Genre.de_json(json_dict, client)

        assert genre.id == id
        assert genre.weight == self.weight
        assert genre.composer_top == self.composer_top
        assert genre.title == self.title
        assert genre.titles == self.titles
        assert genre.images == images
        assert genre.show_in_menu == self.show_in_menu
        assert genre.full_title == self.full_title
        assert genre.url_part == self.url_part
        assert genre.color == self.color
        assert genre.radio_icon == radio_icon
        assert genre.sub_genres == sub_genres
        assert genre.hide_in_regions == self.hide_in_regions

    def test_equality(self):
        pass
