# AGENTS.md

Contributor guide for `fastapi-keycloak`, a Python client that wraps the Keycloak Admin/OIDC API for use with FastAPI.

## Repo layout

- `fastapi_keycloak/` — the package itself.
  - `api.py` — `FastAPIKeycloakAuth` (token validation/decoding, auth flows; no admin credentials) and
    `FastAPIKeycloak` (subclass adding the admin API: user/role/group management, password-grant login).
  - `model.py` — pydantic models for Keycloak resources (`KeycloakUser`, `OIDCUser`, `KeycloakToken`, etc.).
  - `exceptions.py` — `KeycloakError` and the `MandatoryActionException` family.
- `tests/unit/` — fast tests with no external dependencies (mocked HTTP via `responses`, a throwaway RSA keypair
  for signing test JWTs). Run these for quick feedback on any change.
- `tests/integration/` — tests against a real Keycloak + Postgres (via `tests/keycloak_postgres.yaml`). Require
  Docker.
- `docs/` — Sphinx docs (MyST Markdown + `sphinx.ext.autodoc`/`napoleon` for the API reference), built and hosted
  on ReadTheDocs via `.readthedocs.yaml`.
- `.github/workflows/` — CI (`testing.yaml`: lint, unit tests, integration tests, docs build) and release
  (`publish.yml`: build + PyPI trusted publishing on tag pushes).

## Dev setup

```shell
pip install -e .[dev]
```

## Running tests

Unit tests — no setup required, run these first:

```shell
pytest tests/unit
```

Integration tests — require Docker:

```shell
cd tests && ./start_infra.sh && cd ..
pytest tests/integration
cd tests && ./stop_infra.sh
```

Any code contribution should come with tests. Prefer a unit test (mocked, in `tests/unit/`) unless the change is
specifically about behavior that only a real Keycloak instance can exercise.

## Lint & format

```shell
ruff check .
ruff format .
```

Both run in CI (`lint` job) and must pass cleanly.

## Building the docs locally

```shell
pip install -e .[docs]
sphinx-build -b html docs docs/_build/html
```

CI builds with `-W` (warnings-as-errors), so docstring/RST issues should be fixed, not ignored.

## Versioning

The single source of truth for the version is `fastapi_keycloak.__version__` in `fastapi_keycloak/__init__.py`
(consumed dynamically by `pyproject.toml`). Follow semver: bump the major version for breaking changes to the
public API — including changes to the *type* of exceptions raised (e.g. the python-jose → PyJWT migration was a
major bump, since it changed the exception types raised by `token_is_valid`/`get_current_user`/`_decode_token`).

## Supported Python versions

Currently 3.10–3.13. This is declared in four places that must move together on a future bump:

1. `pyproject.toml` — `requires-python` and the `Programming Language :: Python :: 3.x` classifiers.
2. `.github/workflows/testing.yaml` — the `unit-tests` job's `python-version` matrix.
3. `.github/workflows/publish.yml` — the hardcoded build `python-version`.
4. `README.md` — the Python version badges.
