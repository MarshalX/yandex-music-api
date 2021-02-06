from yandex_music import CaseForms


class TestCaseForms:
    nominative = 'Илья'
    genitive = 'Ильи'
    dative = 'Илье'
    accusative = 'Илью'
    instrumental = 'Ильей'
    prepositional = 'Илье'

    def test_expected_values(self, case_forms):
        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_de_json_none(self, client):
        assert CaseForms.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'nominative': self.nominative,
            'genitive': self.genitive,
            'dative': self.dative,
            'accusative': self.accusative,
            'instrumental': self.instrumental,
            'prepositional': self.prepositional,
        }
        case_forms = CaseForms.de_json(json_dict, client)

        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_de_json_all(self, client):
        json_dict = {
            'nominative': self.nominative,
            'genitive': self.genitive,
            'dative': self.dative,
            'accusative': self.accusative,
            'instrumental': self.instrumental,
            'prepositional': self.prepositional,
        }
        case_forms = CaseForms.de_json(json_dict, client)

        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_equality(self):
        a = CaseForms(
            self.nominative, self.genitive, self.dative, self.accusative, self.instrumental, self.prepositional
        )
        b = CaseForms(self.nominative, '', self.dative, self.accusative, self.instrumental, self.prepositional)
        c = CaseForms(
            self.nominative, self.genitive, self.dative, self.accusative, self.instrumental, self.prepositional
        )

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
