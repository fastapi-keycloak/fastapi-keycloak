import jwt
import pytest
import responses
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from fastapi_keycloak import FastAPIKeycloak, FastAPIKeycloakAuth

SERVER_URL = "http://localhost:8085/auth"
REALM = "Test"
REALM_URI = f"{SERVER_URL}/realms/{REALM}"
TOKEN_URI = f"{REALM_URI}/protocol/openid-connect/token"


@pytest.fixture(scope="session")
def rsa_keypair():
    """A throwaway RSA keypair used to sign/verify tokens without a live Keycloak."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


@pytest.fixture
def sign_token(rsa_keypair):
    """Returns a function that signs a claims dict into a JWT using the throwaway keypair."""
    private_pem, _ = rsa_keypair

    def _sign(claims: dict, algorithm: str = "RS256") -> str:
        return jwt.encode(claims, private_pem, algorithm=algorithm)

    return _sign


@pytest.fixture
def idp(monkeypatch, rsa_keypair, sign_token):
    """A FastAPIKeycloak instance backed entirely by mocked HTTP calls, requiring no Docker/network."""
    _, public_pem = rsa_keypair
    monkeypatch.setattr(FastAPIKeycloak, "public_key", property(lambda self: public_pem.decode()))

    admin_token = sign_token(
        {
            "resource_access": {
                "realm-management": {"roles": ["manage-users"]},
                "account": {"roles": ["manage-account"]},
            },
        }
    )

    responses.start()
    responses.add(
        responses.GET,
        f"{REALM_URI}/.well-known/openid-configuration",
        json={
            "token_endpoint": TOKEN_URI,
            "authorization_endpoint": f"{REALM_URI}/protocol/openid-connect/auth",
            "end_session_endpoint": f"{REALM_URI}/protocol/openid-connect/logout",
        },
    )
    responses.add(responses.POST, TOKEN_URI, json={"access_token": admin_token})

    try:
        yield FastAPIKeycloak(
            server_url=SERVER_URL,
            client_id="test-client",
            client_secret="test-client-secret",
            admin_client_secret="test-admin-secret",
            realm=REALM,
            callback_uri="http://localhost:8081/callback",
        )
    finally:
        responses.stop()
        responses.reset()


@pytest.fixture
def idp_auth(monkeypatch, rsa_keypair):
    """A FastAPIKeycloakAuth instance. Unlike `idp`, construction makes no HTTP calls at all — there's
    no admin token to fetch on startup, which is the whole point of the auth-only class."""
    _, public_pem = rsa_keypair
    monkeypatch.setattr(FastAPIKeycloakAuth, "public_key", property(lambda self: public_pem.decode()))

    return FastAPIKeycloakAuth(
        server_url=SERVER_URL,
        client_id="test-client",
        client_secret="test-client-secret",
        realm=REALM,
        callback_uri="http://localhost:8081/callback",
    )
