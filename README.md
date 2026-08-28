# FastAPI Keycloak Integration

![Py3.10](https://img.shields.io/badge/-Python%203.10-brightgreen)
![Py3.11](https://img.shields.io/badge/-Python%203.11-brightgreen)
![Py3.12](https://img.shields.io/badge/-Python%203.12-brightgreen)
![Py3.13](https://img.shields.io/badge/-Python%203.13-brightgreen)

## Introduction

Welcome to `fastapi-keycloak`. This projects goal is to ease the integration of Keycloak (OpenID Connect) with Python, especially FastAPI. FastAPI is not necessary but is
encouraged due to specific features. Currently, this package supports only the `password` and the `authorization_code`. However, the `get_current_user()` method accepts any JWT
that was signed using Keycloak´s private key.

## Installation

```shell
pip install fastapi_keycloak
```

## Usage

```python
from fastapi import FastAPI, Depends
from fastapi_keycloak import FastAPIKeycloak, OIDCUser

app = FastAPI()
idp = FastAPIKeycloak(
    server_url="https://auth.some-domain.com/auth",
    client_id="some-client",
    client_secret="some-secret",
    admin_client_secret="some-admin-cli-secret",
    realm="some-realm-name",
    callback_uri="http://localhost:8081/callback",
)
idp.add_swagger_config(app)


@app.get("/protected")
def protected(user: OIDCUser = Depends(idp.get_current_user())):
    return f"Hi {user}"
```

If your service only needs to authenticate requests (no user/role/group management), use `FastAPIKeycloakAuth`
instead — it requires no `admin_client_secret`:

```python
from fastapi_keycloak import FastAPIKeycloakAuth

idp = FastAPIKeycloakAuth(
    server_url="https://auth.some-domain.com/auth",
    client_id="some-client",
    client_secret="some-secret",
    realm="some-realm-name",
    callback_uri="http://localhost:8081/callback",
)
```

`FastAPIKeycloak` extends `FastAPIKeycloakAuth` with the full admin API, so existing code keeps working unchanged.

## Docs

Docs are available at [https://fastapi-keycloak.readthedocs.io/](https://fastapi-keycloak.readthedocs.io/).

## TLDR

FastAPI Keycloak enables you to do the following things without writing a single line of additional code:

- Verify identities and roles of users with Keycloak
- Get a list of available identity providers
- Create/read/delete users
- Create/read/delete roles
- Create/read/delete/assign groups (recursive). Thanks to @fabiothz
- Assign/remove roles from users
- Implement the `password` or the `authorization_code` flow (login/callback/logout)

## Contributions

We would like encourage anyone using this package to contribute to its improvement, if anything isn't working as expected or isn't well enough documented, please open an issue or a
pull request. Please note that for any code contribution tests are required. See [AGENTS.md](AGENTS.md) for the full contributor guide, including how to run the test suite,
lint/format the code, and build the docs locally.

## Original authors

Shoutout to the original authors of this project:

- Yannic Schröer @yannicschroeer
- Jonas Scholl @JonasScholl

This project was in the [Code Specialist organization](https://github.com/code-specialist/) before being moved here.
