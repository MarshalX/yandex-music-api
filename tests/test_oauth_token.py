from typing import Dict

from yandex_music import Client, JSONType, OAuthToken


class TestOAuthToken:
    access_token = 'y0_AgAAAABexampleAAAAAA...'
    refresh_token = '1:refreshexample'
    expires_in = 31536000
    token_type = 'bearer'

    def test_expected_values(self, oauth_token: OAuthToken) -> None:
        assert oauth_token.access_token == self.access_token
        assert oauth_token.refresh_token == self.refresh_token
        assert oauth_token.expires_in == self.expires_in
        assert oauth_token.token_type == self.token_type

    def test_de_json_none(self, client: Client) -> None:
        assert OAuthToken.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'access_token': self.access_token}
        token = OAuthToken.de_json(json_dict, client)
        assert token is not None

        assert token.access_token == self.access_token
        assert token.refresh_token is None
        assert token.expires_in is None
        assert token.token_type is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': self.expires_in,
            'token_type': self.token_type,
        }
        token = OAuthToken.de_json(json_dict, client)
        assert token is not None

        assert token.access_token == self.access_token
        assert token.refresh_token == self.refresh_token
        assert token.expires_in == self.expires_in
        assert token.token_type == self.token_type

    def test_equality(self) -> None:
        a = OAuthToken('tok_a')
        b = OAuthToken('tok_b')
        c = OAuthToken('tok_a')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
