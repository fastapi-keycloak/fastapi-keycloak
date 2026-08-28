from datetime import datetime, timedelta, timezone

import jwt
import pytest


def test_decode_token_valid(idp, sign_token):
    token = sign_token({"sub": "user-1", "aud": "account"})
    decoded = idp._decode_token(token, audience="account")
    assert decoded["sub"] == "user-1"


def test_decode_token_expired(idp, sign_token):
    expired_at = datetime.now(timezone.utc) - timedelta(hours=1)
    token = sign_token({"sub": "user-1", "exp": expired_at})
    with pytest.raises(jwt.ExpiredSignatureError):
        idp._decode_token(token)


def test_decode_token_wrong_audience(idp, sign_token):
    token = sign_token({"sub": "user-1", "aud": "some-other-client"})
    with pytest.raises(jwt.PyJWTError):
        idp._decode_token(token, audience="account")


def test_decode_token_malformed(idp):
    with pytest.raises(jwt.PyJWTError):
        idp._decode_token("not-a-token")


def test_decode_token_wrong_algorithm(idp, rsa_keypair):
    private_pem, _ = rsa_keypair
    token = jwt.encode({"sub": "user-1"}, "some-hmac-secret", algorithm="HS256")
    with pytest.raises(jwt.InvalidAlgorithmError):
        idp._decode_token(token)


def test_token_is_valid_true(idp, sign_token):
    token = sign_token({"sub": "user-1"})
    assert idp.token_is_valid(token) is True


def test_token_is_valid_false(idp):
    assert idp.token_is_valid("not-a-token") is False
