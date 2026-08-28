# FastAPI Keycloak Integration

[![codecov](https://codecov.io/gh/fastapi-keycloak/fastapi-keycloak/branch/main/graph/badge.svg)](https://codecov.io/gh/fastapi-keycloak/fastapi-keycloak)

```{toctree}
:hidden:
:maxdepth: 2

quickstart
keycloak_configuration
full_example
reference
known_issues
```

## Introduction

Welcome to `fastapi-keycloak`. This project's goal is to ease the integration of Keycloak (OpenID Connect) with
Python, especially FastAPI. FastAPI is not necessary but is encouraged due to specific features. Currently, this
package supports only the `password` and the `authorization_code` flow. However, the `get_current_user()` method
accepts any JWT that was signed using Keycloak's private key.

The package exposes two client classes:

- [`FastAPIKeycloakAuth`](reference.md#fastapikeycloakauth) — token validation only (`get_current_user()`,
  `token_is_valid()`, the authorization_code flow). No admin credentials required.
- [`FastAPIKeycloak`](reference.md#fastapikeycloak) — extends `FastAPIKeycloakAuth` with the full admin API
  (user/role/group management, password-grant login). Requires an `admin_client_secret`.

Use `FastAPIKeycloakAuth` if your service only needs to authenticate requests; use `FastAPIKeycloak` if it also
needs to manage users, roles, or groups.

## Installation

```shell
pip install fastapi_keycloak
```

## TLDR;

FastAPI Keycloak enables you to do the following things without writing a single line of additional code:

- Verify identities and roles of users with Keycloak
- Get a list of available identity providers
- Create/read/delete users
- Create/read/delete groups
- Create/read/delete roles
- Assign/remove roles from users
- Assign/remove users from groups
- Implement the `password` or the `authorization_code` flow (login/callback/logout)

## Example

This example assumes you use a frontend technology (such as React, Vue, or whatever suits you) to render your pages
and merely depicts a `protected backend`.

### app.py

```{literalinclude} examples/introduction/app.py
:language: python
```
