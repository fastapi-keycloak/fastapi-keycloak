import pytest

from fastapi_keycloak.exceptions import KeycloakError
from fastapi_keycloak.model import KeycloakToken, OIDCUser


def _oidc_user(**overrides):
    defaults = dict(sub="user-1", iat=0, exp=0, email_verified=True)
    defaults.update(overrides)
    return OIDCUser(**defaults)


def test_oidc_user_roles_from_realm_access():
    user = _oidc_user(realm_access={"roles": ["admin"]})
    assert user.roles == ["admin"]


def test_oidc_user_roles_from_resource_access():
    user = _oidc_user(azp="my-client", resource_access={"my-client": {"roles": ["viewer"]}})
    assert user.roles == ["viewer"]


def test_oidc_user_roles_combines_both_sources():
    user = _oidc_user(
        realm_access={"roles": ["admin"]},
        azp="my-client",
        resource_access={"my-client": {"roles": ["viewer"]}},
    )
    assert set(user.roles) == {"admin", "viewer"}


def test_oidc_user_roles_missing_raises():
    user = _oidc_user()
    with pytest.raises(KeycloakError):
        _ = user.roles


def test_oidc_user_str_is_preferred_username():
    user = _oidc_user(preferred_username="alice")
    assert str(user) == "alice"


def test_keycloak_token_str_is_bearer_header():
    token = KeycloakToken(access_token="abc123")
    assert str(token) == "Bearer abc123"
