# API Reference

## FastAPIKeycloakAuth

Token validation only — no admin credentials required. Use this if you only need `get_current_user()` /
`token_is_valid()` and the authorization_code flow.

```{eval-rst}
.. autoclass:: fastapi_keycloak.FastAPIKeycloakAuth
   :members:
   :undoc-members:
   :show-inheritance:
```

## FastAPIKeycloak

Extends `FastAPIKeycloakAuth` with the full Keycloak admin API (user/role/group management, password-grant login).
Requires an `admin_client_secret`.

```{eval-rst}
.. autoclass:: fastapi_keycloak.FastAPIKeycloak
   :members:
   :undoc-members:
   :show-inheritance:
```

## Exceptions

```{eval-rst}
.. automodule:: fastapi_keycloak.exceptions
   :members:
   :show-inheritance:
```

## Models

```{eval-rst}
.. automodule:: fastapi_keycloak.model
   :members:
   :show-inheritance:
```
