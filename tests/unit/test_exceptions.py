import pytest

from fastapi_keycloak.exceptions import (
    ConfigureTOTPException,
    KeycloakError,
    MandatoryActionException,
    UpdatePasswordException,
    UpdateProfileException,
    UpdateUserLocaleException,
    UserNotFound,
    VerifyEmailException,
)


def test_keycloak_error_carries_status_and_reason():
    error = KeycloakError(status_code=404, reason="not found")
    assert error.status_code == 404
    assert error.reason == "not found"
    assert str(error) == "HTTP 404: not found"


def test_user_not_found_carries_status_and_reason():
    error = UserNotFound(status_code=404, reason="no such user")
    assert error.status_code == 404
    assert error.reason == "no such user"


@pytest.mark.parametrize(
    "exception_cls",
    [
        UpdateUserLocaleException,
        ConfigureTOTPException,
        VerifyEmailException,
        UpdatePasswordException,
        UpdateProfileException,
    ],
)
def test_mandatory_action_exceptions_are_http_400(exception_cls):
    error = exception_cls()
    assert isinstance(error, MandatoryActionException)
    assert error.status_code == 400
    assert error.detail
