from yandex_music import Concert


class TestConcert:
    id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    images = [
        'https://avatars.mds.yandex.net/get-afisha/1234/image1',
        'https://avatars.mds.yandex.net/get-afisha/1234/image2',
    ]
    image_url = 'https://avatars.mds.yandex.net/get-afisha/1234/main'
    concert_title = 'Большой весенний концерт'
    afisha_url = 'https://afisha.yandex.ru/event/a1b2c3d4-e5f6'
    city = 'Москва'
    place = 'Крокус Сити Холл'
    address = 'МКАД, 65-66 км'
    datetime = '2026-06-15T19:00:00+03:00'
    content_rating = '16+'

    def test_expected_value(self, concert, concert_min_price, concert_cashback, concert_event_info):
        assert concert.id == self.id
        assert concert.images == self.images
        assert concert.image_url == self.image_url
        assert concert.concert_title == self.concert_title
        assert concert.afisha_url == self.afisha_url
        assert concert.city == self.city
        assert concert.place == self.place
        assert concert.address == self.address
        assert concert.datetime == self.datetime
        assert concert.content_rating == self.content_rating
        assert concert.min_price == concert_min_price
        assert concert.cashback == concert_cashback
        assert concert.event_info == concert_event_info

    def test_de_json_none(self, client):
        assert Concert.de_json({}, client) is None

    def test_de_json_all(self, client, concert_min_price, concert_cashback, concert_event_info):
        json_dict = {
            'id': self.id,
            'images': self.images,
            'image_url': self.image_url,
            'concert_title': self.concert_title,
            'afisha_url': self.afisha_url,
            'city': self.city,
            'place': self.place,
            'address': self.address,
            'datetime': self.datetime,
            'content_rating': self.content_rating,
            'min_price': concert_min_price.to_dict(),
            'cashback': concert_cashback.to_dict(),
            'event_info': concert_event_info.to_dict(),
        }
        concert = Concert.de_json(json_dict, client)

        assert concert.id == self.id
        assert concert.images == self.images
        assert concert.image_url == self.image_url
        assert concert.concert_title == self.concert_title
        assert concert.afisha_url == self.afisha_url
        assert concert.city == self.city
        assert concert.place == self.place
        assert concert.address == self.address
        assert concert.datetime == self.datetime
        assert concert.content_rating == self.content_rating
        assert concert.min_price == concert_min_price
        assert concert.cashback == concert_cashback
        assert concert.event_info == concert_event_info

    def test_equality(self):
        a = Concert(id=self.id)
        b = Concert(id='different-uuid-here')
        c = Concert(id=self.id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
