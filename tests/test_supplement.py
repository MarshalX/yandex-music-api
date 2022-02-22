import pytest

from yandex_music import Supplement


@pytest.fixture(scope='class')
def supplement(lyrics, video_supplement):
    return Supplement(
        TestSupplement.id, lyrics, [video_supplement], TestSupplement.radio_is_available, TestSupplement.description
    )


class TestSupplement:
    id = 103844
    radio_is_available = False
    description = (
        '"ИНТЕРВЬЮ С КОМИКОМ" - это не юмористический проект. Это разговор о жизни, творчестве, интересах, '
        'целях и приоритетах, о том, кто как живет и почему.\nНовый проект Дмитрия Романова, в котором он '
        'берет интервью.\n Гость выпуска - комик Нурлан Сабуров'
    )

    def test_expected_values(self, supplement, lyrics, video_supplement):
        assert supplement.id == self.id
        assert supplement.lyrics == lyrics
        assert supplement.videos == [video_supplement]
        assert supplement.radio_is_available == self.radio_is_available
        assert supplement.description == self.description

    def test_de_json_none(self, client):
        assert Supplement.de_json({}, client) is None

    def test_de_json_required(self, client, lyrics, video_supplement):
        json_dict = {'id': self.id, 'lyrics': lyrics.to_dict(), 'videos': [video_supplement.to_dict()]}
        supplement = Supplement.de_json(json_dict, client)

        assert supplement.id == self.id
        assert supplement.lyrics == lyrics
        assert supplement.videos == [video_supplement]

    def test_de_json_all(self, client, lyrics, video_supplement):
        json_dict = {
            'id': self.id,
            'lyrics': lyrics.to_dict(),
            'videos': [video_supplement.to_dict()],
            'radio_is_available': self.radio_is_available,
            'description': self.description,
        }
        supplement = Supplement.de_json(json_dict, client)

        assert supplement.id == self.id
        assert supplement.lyrics == lyrics
        assert supplement.videos == [video_supplement]
        assert supplement.radio_is_available == self.radio_is_available
        assert supplement.description == self.description

    def test_equality(self, lyrics, video_supplement):
        a = Supplement(self.id, lyrics, [video_supplement])
        b = Supplement(self.id, None, [video_supplement])
        c = Supplement(self.id, lyrics, [video_supplement])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
