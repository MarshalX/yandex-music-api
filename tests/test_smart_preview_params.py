from yandex_music import SmartPreviewParams


class TestSmartPreviewParams:
    duration_ms = 17700

    def test_expected_value(self, smart_preview_params, fade):
        assert smart_preview_params.duration_ms == self.duration_ms
        assert smart_preview_params.fade == fade

    def test_de_json_none(self, client):
        assert SmartPreviewParams.de_json({}, client) is None

    def test_de_json_all(self, client, fade):
        json_dict = {
            'durationMs': self.duration_ms,
            'fade': fade.to_dict(),
        }
        smart_preview_params = SmartPreviewParams.de_json(json_dict, client)

        assert smart_preview_params.duration_ms == self.duration_ms
        assert smart_preview_params.fade == fade

    def test_equality(self, fade):
        a = SmartPreviewParams(duration_ms=self.duration_ms, fade=fade)
        b = SmartPreviewParams(duration_ms=10000, fade=fade)
        c = SmartPreviewParams(duration_ms=self.duration_ms, fade=fade)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
