import jwt
import pytest
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from fastapi_keycloak import HTTPMethod
from fastapi_keycloak.model import KeycloakRole


class TestAPIIntegration:
    def test_properties(self, idp):
        assert idp.public_key
        assert idp.admin_token
        assert idp.open_id_configuration
        assert idp.logout_uri
        assert idp.login_uri
        assert idp.roles_uri
        assert idp.token_uri
        assert idp.authorization_uri
        assert idp.user_auth_scheme
        assert idp.providers_uri
        assert idp.realm_uri
        assert idp.users_uri

    def test_admin_token(self, idp):
        assert idp.admin_token
        with pytest.raises(jwt.DecodeError):  # Not enough segments
            idp.admin_token = "some rubbish"

        with pytest.raises(jwt.InvalidAlgorithmError):  # HS256 token, RS256-only algorithms
            idp.admin_token = """
            eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
            """

    def test_add_swagger_config(self, idp):
        app = FastAPI()
        assert app.swagger_ui_init_oauth is None
        idp.add_swagger_config(app)
        assert app.swagger_ui_init_oauth == {
            "usePkceWithAuthorizationCodeGrant": True,
            "clientId": idp.client_id,
            "clientSecret": idp.client_secret,
        }

    def test_user_auth_scheme(self, idp):
        assert isinstance(idp.user_auth_scheme, OAuth2PasswordBearer)

    def test_open_id_configuration(self, idp):
        assert idp.open_id_configuration
        assert isinstance(idp.open_id_configuration, dict)

    def test_proxy(self, idp):
        response = idp.proxy(relative_path="/realms/Test", method=HTTPMethod.GET)
        assert isinstance(response.json(), dict)

    def test_get_all_roles_and_get_roles(self, idp):
        roles: list[KeycloakRole] = idp.get_all_roles()
        assert roles
        lookup = idp.get_roles(role_names=[role.name for role in roles])
        assert lookup
        assert len(roles) == len(lookup)

    def test_get_identity_providers(self, idp):
        assert idp.get_identity_providers() == []
