#!/bin/bash
set -eux

# Keycloak 26+ defaults the built-in `admin-cli` client to "Always use lightweight access
# token" (client.use.lightweight.access.token.enabled=true), which strips the
# `resource_access` claim that fastapi_keycloak relies on to verify the admin token has
# realm-management/account access. This default is re-applied by Keycloak's realm importer
# for reserved/built-in clients regardless of what realm-export.json specifies, so it has to
# be disabled after the server is up via the Admin REST API instead.

declare URL=${1:-http://localhost:8085}
declare REALM=${2:-Test}
declare BOOTSTRAP_USERNAME=${3:-keycloakuser}
declare BOOTSTRAP_PASSWORD=${4:-keycloakpassword}

ADMIN_TOKEN=$(curl -sf -X POST "${URL}/auth/realms/master/protocol/openid-connect/token" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "client_id=admin-cli&username=${BOOTSTRAP_USERNAME}&password=${BOOTSTRAP_PASSWORD}&grant_type=password" \
    | python3 -c 'import json, sys; print(json.load(sys.stdin)["access_token"])')

CLIENT_UUID=$(curl -sf -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "${URL}/auth/admin/realms/${REALM}/clients?clientId=admin-cli" \
    | python3 -c 'import json, sys; print(json.load(sys.stdin)[0]["id"])')

curl -sf -o /dev/null -X PUT \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H 'Content-Type: application/json' \
    "${URL}/auth/admin/realms/${REALM}/clients/${CLIENT_UUID}" \
    -d '{"attributes": {"client.use.lightweight.access.token.enabled": "false"}}'

echo "disabled lightweight access tokens for admin-cli in realm ${REALM}"
