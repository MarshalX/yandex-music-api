from yandex_music import CaseForms


class TestCaseForms:
    nominative = None
    genitive = None
    dative = None
    accusative = None
    instrumental = None
    prepositional = None

    def test_expected_values(self, case_forms):
        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_de_json_required(self, client):
        json_dict = {'nominative': self.nominative, 'genitive': self.genitive, 'dative': self.dative,
                     'accusative': self.accusative, 'instrumental': self.instrumental,
                     'prepositional': self.prepositional}
        case_forms = CaseForms.de_json(json_dict, client)

        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_de_json_all(self, client):
        json_dict = {'nominative': self.nominative, 'genitive': self.genitive, 'dative': self.dative,
                     'accusative': self.accusative, 'instrumental': self.instrumental,
                     'prepositional': self.prepositional}
        case_forms = CaseForms.de_json(json_dict, client)

        assert case_forms.nominative == self.nominative
        assert case_forms.genitive == self.genitive
        assert case_forms.dative == self.dative
        assert case_forms.accusative == self.accusative
        assert case_forms.instrumental == self.instrumental
        assert case_forms.prepositional == self.prepositional

    def test_equality(self):
        pass
