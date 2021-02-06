from yandex_music import MetaData


class TestMetaData:
    album = 'VK Virus Bot'
    volume = 1
    year = 2018
    number = 6
    genre = 'Techno'
    lyricist = (
        'Можете величать меня исчадьем ада\nМожете линчевать меня, мыча как стадо\nНо на мне нет печати зла, '
        'сгущать не надо\nКраски. Я счастлив, что я не раб мещанских взглядов\nМожете обличать меня, крича с экрана'
        '\nМожете исключать меня из ваших кланов\nНо вы же сами не без греха. Признай, что я был\nК несчастью таким'
        ' же, как ты. Ша!\nМолчать и на пол!\n\nСложней всего было найти тротил и запал\nИ пронести на бал, фитиль'
        ' был подозрительно мал\nАктовый зал, АК достал, с предохранителя снял\nКак удивится директриса, лишь'
        ' увидев меня\nОдиннадцатый "А", не хотите мира - выйдет война\nНет, я не маньяк, при чем здесь Чикатило,'
        ' Битцевский парк?\nТерроризма признанный акт - для других единственный шанс\nЕстественный шаг - объявить'
        ' обидчикам личный джихад\nЯ терпеливо ждал, но что делать - мой класс - педики\nЖертвы маркетинга,'
        ' масс-медиа и косметики\nВы все в ответе за то несчастье, что сейчас светит вам\nПоследний звонок,'
        ' в шейный позвонок мой глаз метит вам!\nЗахожу без шума и спецэффектов - им деться некуда\nПалю известной'
        ' в школе сердцеедке в сердце метко:\nПрости золотая, но врачи тебя не залатают\nНехуй рвать мои письма - '
        'толпа бежит из зала, тая\n\nМожете величать меня исчадьем ада\nМожете линчевать меня, мыча как стадо\nНо '
        'на мне нет печати зла, сгущать не надо\nКраски. Я счастлив, что я не раб мещанских взглядов\nМожете '
        'обличать меня, крича с экрана\nМожете исключать меня из ваших кланов\nНо вы же сами не без греха. '
        'Признай, что я был\nК несчастью таким же, как ты. Ша!\nМолчать и на пол!\n\nШарики, ленты, рядышком '
        'двоечник и отличник\nСтонущий от боли обидчик - что может быть еще мелодичней?\nТе, кто свинцом не '
        'напичкан забаррикадировались в коридоре\nЯ перезарядил, проверяю затвор\nИ стреляю в упор. Иду гулять по '
        'школе\nЯ не сатанист, не фанат металла, влом\nБыть таким. Их стволы - металлолом\nНе псих, не фрик, не '
        'играл давно за компом\nТак что не верь ментам, народ\nЖизнь, как игра в домино\nВсем важно одно - забить '
        'отпущенья козла\nВы мне мученье доставили, но ваш час быть мишенью настал!\nВремя замедляет свой бег\nЯ '
        'не понимаю кто стреляет по мне\nГде-то падает дверь\nA la guerre comme а la guerre,\nСнайперы мелькают в '
        'окне\nИз меня что-то начинает течь\nВезде томатный кетчуп, мне обеспечена вечность\nВ руке детонатор...\n'
        'Я просыпаюсь рывком, покрыт испариной лоб -\nКошмар, а не сон, в кровати жарко - я шагаю во двор\n'
        'Спускаюсь в погреб,отпираю ржавый медный замок\nИ собираю ствол АК - завтра последний звонок...\n\n'
        'Можете величать меня исчадьем ада\nМожете линчевать меня, мыча как стадо\nНо на мне нет печати зла, '
        'сгущать не надо\nКраски. Я счастлив, что я не раб мещанских взглядов\nМожете обличать меня, крича с экрана'
        '\nМожете исключать меня из ваших кланов\nНо вы же сами не без греха. Признай, что я был\nК несчастью таким'
        ' же, как ты. Ша!\nМолчать и на пол!\n\nСпасибо Kaas\'у, так что не смейте обвинять меня в плагиате\nВсе'
        ' сейчас на Одноклассниках, ВКонтакте\nНо далеко не все одноклассники в контакте\nПонимаете, о чем идет'
        ' речь?\nЙее, Оксимирон. В Лондоне наконец-то солнце'
    )
    version = 'Provided to YouTube by Pias UK Limited'
    composer = 'oXEfhutXNHU'

    def test_expected_values(self, meta_data):
        assert meta_data.album == self.album
        assert meta_data.volume == self.volume
        assert meta_data.year == self.year
        assert meta_data.number == self.number
        assert meta_data.genre == self.genre
        assert meta_data.lyricist == self.lyricist
        assert meta_data.version == self.version
        assert meta_data.composer == self.composer

    def test_de_json_none(self, client):
        assert MetaData.de_json({}, client) is None

    def test_de_json_required(self, client):
        MetaData.de_json({}, client)

    def test_de_json_all(self, client):
        json_dict = {
            'album': self.album,
            'volume': self.volume,
            'year': self.year,
            'number': self.number,
            'genre': self.genre,
            'lyricist': self.lyricist,
            'version': self.version,
            'composer': self.composer,
        }
        meta_data = MetaData.de_json(json_dict, client)

        assert meta_data.album == self.album
        assert meta_data.volume == self.volume
        assert meta_data.year == self.year
        assert meta_data.number == self.number
        assert meta_data.genre == self.genre
        assert meta_data.lyricist == self.lyricist
        assert meta_data.version == self.version
        assert meta_data.composer == self.composer

    def test_equality(self):
        a = MetaData(self.album, self.volume, self.year)
        b = MetaData(self.album, 0, 2016)
        c = MetaData(self.album, self.volume, self.year)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
