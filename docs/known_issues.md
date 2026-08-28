# Known issues

## Apple Silicon (M1/M2/M3)

Older Keycloak images (pre-`quay.io/keycloak/keycloak`, i.e. the legacy `jboss/keycloak` images) were not published
for `arm64` and would fail to start on Apple Silicon without rebuilding the image locally. The image used by
`tests/keycloak_postgres.yaml` (`quay.io/keycloak/keycloak:25.0`) is published as a multi-arch image and runs
natively on Apple Silicon, so this workaround should no longer be necessary. If you do hit a startup issue on
Apple Silicon with a newer Keycloak image, please open an issue with the details.
