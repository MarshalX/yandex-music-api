from yandex_music import YandexMusicObject


class Genre(YandexMusicObject):
    def __init__(self,
                 id,
                 weight,
                 composer_top,
                 title,
                 titles,
                 images,
                 show_in_menu,
                 full_title=None,
                 url_part=None,
                 color=None,
                 radio_icon=None,
                 sub_genres=None,
                 hide_in_regions=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.weight = weight
        self.composer_top = composer_top
        self.title = title
        self.titles = titles
        self.images = images
        self.show_in_menu = show_in_menu

        self.full_title = full_title
        self.url_part = url_part
        self.color = color
        self.radio_icon = radio_icon
        self.sub_genres = sub_genres
        self.hide_in_regions = hide_in_regions

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Genre, cls).de_json(data, client)
        from yandex_music import Title, Icon, Images
        data['titles'] = Title.de_dict(data.get('titles'), client)
        data['images'] = Images.de_json(data.get('images'), client)
        data['radio_icon'] = Icon.de_json(data.get('radio_icon'), client)
        data['sub_genres'] = Genre.de_list(data.get('sub_genres'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        genres = list()
        for genre in data:
            genres.append(cls.de_json(genre, client))

        return genres
