from yandex_music import OpenGraphData


class TestOpenGraphData:
    title = 'Подкасты недели'
    description = (
        'Чтобы собрать для вас этот плейлист, мы должны узнать вас '
        'чуточку поближе. Заходите на Музыку и слушайте больше!'
    )

    def test_expected_values(self, open_graph_data, cover):
        assert open_graph_data.title == self.title
        assert open_graph_data.description == self.description

    def test_de_json_none(self, client):
        assert OpenGraphData.de_json({}, client) is None

    def test_de_json_required(self, client, cover):
        json_dict = {'title': self.title, 'description': self.description, 'image': cover.to_dict()}
        open_graph_data = OpenGraphData.de_json(json_dict, client)

        assert open_graph_data.title == self.title
        assert open_graph_data.description == self.description
        assert open_graph_data.image == cover

    def test_de_json_all(self, client, cover):
        json_dict = {'title': self.title, 'description': self.description, 'image': cover.to_dict()}
        open_graph_data = OpenGraphData.de_json(json_dict, client)

        assert open_graph_data.title == self.title
        assert open_graph_data.description == self.description
        assert open_graph_data.image == cover

    def test_equality(self, cover):
        a = OpenGraphData(self.title, self.description, cover)
        b = OpenGraphData('', self.description, cover)
        c = OpenGraphData(self.title, self.description, cover)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
