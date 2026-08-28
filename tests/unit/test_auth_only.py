import pytest
import responses

from fastapi_keycloak import FastAPIKeycloak, FastAPIKeycloakAuth


def test_construction_requires_no_admin_secret(idp_auth):
    assert not hasattr(idp_auth, "admin_client_secret")
    assert idp_auth.algorithms == "RS256"


def test_fastapikeycloak_is_a_fastapikeycloakauth(idp):
    assert isinstance(idp, FastAPIKeycloakAuth)
    assert isinstance(idp, FastAPIKeycloak)


def test_fastapikeycloakauth_is_not_a_fastapikeycloak(idp_auth):
    assert isinstance(idp_auth, FastAPIKeycloakAuth)
    assert not isinstance(idp_auth, FastAPIKeycloak)


@pytest.mark.parametrize(
    "admin_only_attr",
    ["admin_token", "proxy", "create_user", "get_all_users", "_get_admin_token", "user_login"],
)
def test_auth_only_class_has_no_admin_surface(idp_auth, admin_only_attr):
    assert not hasattr(idp_auth, admin_only_attr)


@pytest.mark.parametrize(
    "shared_attr",
    ["get_current_user", "token_is_valid", "_decode_token", "public_key", "exchange_authorization_code", "login_uri"],
)
def test_admin_class_still_has_the_auth_only_surface(idp, shared_attr):
    assert hasattr(idp, shared_attr)


def test_token_is_valid_via_auth_only_class(idp_auth, sign_token):
    token = sign_token({"sub": "user-1"})
    assert idp_auth.token_is_valid(token) is True
    assert idp_auth.token_is_valid("not-a-token") is False


@responses.activate
def test_get_current_user_via_auth_only_class(idp_auth, sign_token):
    # get_current_user() builds an OAuth2PasswordBearer(tokenUrl=self.token_uri) for Swagger's benefit,
    # which requires fetching the OIDC discovery document even though decoding itself only needs the
    # (already-mocked) public key. This is true for both classes, not something the split introduced.
    responses.add(
        responses.GET,
        f"{idp_auth.realm_uri}/.well-known/openid-configuration",
        json={"token_endpoint": f"{idp_auth.realm_uri}/protocol/openid-connect/token"},
    )

    token = sign_token(
        {
            "sub": "user-1",
            "aud": "account",
            "iat": 0,
            "exp": 9999999999,
            "email_verified": True,
            "preferred_username": "alice",
            "realm_access": {"roles": ["default-roles-test"]},
        }
    )
    current_user = idp_auth.get_current_user()
    user = current_user(token=token)
    assert user.sub == "user-1"
    assert "default-roles-test" in user.roles
