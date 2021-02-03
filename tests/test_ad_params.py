from yandex_music import AdParams


class TestAdParams:
    partner_id = '146552'
    category_id = '0'
    page_ref = 'http://music.yandex.ru'
    target_ref = 'http://music.yandex.ru'
    other_params = 'user:561231028'
    ad_volume = -15
    genre_id = None
    genre_name = None

    def test_expected_values(self, ad_params):
        assert ad_params.partner_id == self.partner_id
        assert ad_params.category_id == self.category_id
        assert ad_params.page_ref == self.page_ref
        assert ad_params.target_ref == self.target_ref
        assert ad_params.other_params == self.other_params
        assert ad_params.ad_volume == self.ad_volume
        assert ad_params.genre_id == self.genre_id
        assert ad_params.genre_name == self.genre_name

    def test_de_json_none(self, client):
        assert AdParams.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'partner_id': self.partner_id,
            'category_id': self.category_id,
            'page_ref': self.page_ref,
            'target_ref': self.target_ref,
            'other_params': self.other_params,
            'ad_volume': self.ad_volume,
        }
        ad_params = AdParams.de_json(json_dict, client)

        assert ad_params.partner_id == self.partner_id
        assert ad_params.category_id == self.category_id
        assert ad_params.page_ref == self.page_ref
        assert ad_params.target_ref == self.target_ref
        assert ad_params.other_params == self.other_params
        assert ad_params.ad_volume == self.ad_volume

    def test_de_json_all(self, client):
        json_dict = {
            'partner_id': self.partner_id,
            'category_id': self.category_id,
            'page_ref': self.page_ref,
            'target_ref': self.target_ref,
            'other_params': self.other_params,
            'ad_volume': self.ad_volume,
            'genre_id': self.genre_id,
            'genre_name': self.genre_name,
        }
        ad_params = AdParams.de_json(json_dict, client)

        assert ad_params.partner_id == self.partner_id
        assert ad_params.category_id == self.category_id
        assert ad_params.page_ref == self.page_ref
        assert ad_params.target_ref == self.target_ref
        assert ad_params.other_params == self.other_params
        assert ad_params.ad_volume == self.ad_volume
        assert ad_params.genre_id == self.genre_id
        assert ad_params.genre_name == self.genre_name

    def test_equality(self):
        a = AdParams(
            self.partner_id, self.category_id, self.page_ref, self.target_ref, self.other_params, self.ad_volume
        )
        b = AdParams(self.partner_id, '10', self.page_ref, self.target_ref, self.other_params, self.ad_volume)
        c = AdParams(self.partner_id, self.category_id, '', self.target_ref, self.other_params, -30)
        d = AdParams(
            self.partner_id, self.category_id, self.page_ref, self.target_ref, self.other_params, self.ad_volume
        )

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
