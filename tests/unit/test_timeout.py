import pytest
import responses
from requests import ReadTimeout

from fastapi_keycloak import HTTPMethod


def test_timeout(idp):
    responses.add(responses.GET, f"{idp.server_url}/timeout", body=ReadTimeout())
    idp.timeout = 0.5

    with pytest.raises(ReadTimeout):
        idp.proxy(relative_path="/timeout", method=HTTPMethod.GET)
