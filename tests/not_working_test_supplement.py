import pytest

from yandex_music import Supplement


@pytest.fixture(scope='class')
def supplement(lyrics, videos):
    return Supplement(TestSupplement.id, lyrics, videos, TestSupplement.radio_is_available)


class TestSupplement:
    radio_is_available = None

    def test_expected_values(self, supplement, id, lyrics, videos):
        assert supplement.id == id
        assert supplement.lyrics == lyrics
        assert supplement.videos == videos
        assert supplement.radio_is_available == self.radio_is_available

    def test_de_json_required(self, client, id, lyrics, videos):
        json_dict = {'id': id, 'lyrics': lyrics, 'videos': videos, 'radio_is_available': self.radio_is_available}
        supplement = Supplement.de_json(json_dict, client)

        assert supplement.id == id
        assert supplement.lyrics == lyrics
        assert supplement.videos == videos
        assert supplement.radio_is_available == self.radio_is_available

    def test_de_json_all(self, client, id, lyrics, videos):
        json_dict = {'id': id, 'lyrics': lyrics, 'videos': videos, 'radio_is_available': self.radio_is_available}
        supplement = Supplement.de_json(json_dict, client)

        assert supplement.id == id
        assert supplement.lyrics == lyrics
        assert supplement.videos == videos
        assert supplement.radio_is_available == self.radio_is_available

    def test_equality(self):
        pass
