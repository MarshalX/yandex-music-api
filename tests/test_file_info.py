from yandex_music import FileInfo


class TestFileInfo:
    def test_expected_values(self, file_info, file_download_info):
        assert file_info.download_info == file_download_info

    def test_de_json_none(self, client):
        assert FileInfo.de_json({}, client) is None

    def test_de_json_all(self, client, file_download_info):
        json_dict = {'downloadInfo': file_download_info.to_dict()}
        file_info = FileInfo.de_json(json_dict, client)

        assert file_info.download_info == file_download_info

    def test_equality(self, file_download_info):
        a = FileInfo(download_info=file_download_info)
        b = FileInfo(download_info=None)
        c = FileInfo(download_info=file_download_info)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
