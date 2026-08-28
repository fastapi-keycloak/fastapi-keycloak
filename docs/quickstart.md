# Quickstart

In order to just get started, we prepared some containers and configs for you.

```{note}
If you have cloned the git repo, you can run this from the `docs/examples/quickstart` directory.
```

## 1. Configure the Containers

**docker-compose.yaml**

```{literalinclude} examples/quickstart/docker-compose.yaml
:language: yaml
```

This will create a Postgres and a Keycloak container ready to use. Make sure to download the
[realm-export.json](examples/quickstart/realm-export.json) and keep it in the same folder as the docker compose file
to bind the configuration.

```{caution}
These containers are stateless and non-persistent. Data will be lost on restart.
```

## 2. Start the Containers

Start the containers by applying the `docker-compose.yaml`:

```shell
docker compose up -d
```

```{note}
When you want to delete the containers you may use `docker compose down` in the same directory to kill the
containers created with the `docker-compose.yaml`.
```

## 3. The FastAPI App

You may use the code below without altering it, the imported config will match these values:

```{literalinclude} examples/quickstart/app.py
:language: python
```

## 4. Usage

You may now use any of the [API's exposed endpoints](reference.md) as everything is configured for testing all the
features.

After you call the `/login` endpoint of your app, you will be redirected to the login screen of Keycloak. You may
open the Keycloak Frontend at [http://localhost:8085/auth](http://localhost:8085/auth) and create a user. To log
into your Keycloak instance, the username is `keycloakuser` and the password is `keycloakpassword` as described in
the `docker-compose.yaml` above.

To utilize this fully you need a way to store the Access-Token provided by the callback route and add it to any
further requests as `Authorization` Bearer.

You can test this with curl like so:

```shell
# TOKEN should be changed to the value of 'access_token'.
# This can be acquired once you have visited http://localhost:8081/login

TOKEN="<your-access-token>"

curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://localhost:8081/user
```

### Refreshing your token

Once your access token expires, you can use the refresh token (that you got along with the access token) to get a
new one.

```shell
# REFRESH_TOKEN should be changed to the value of 'refresh_token'.
REFRESH_TOKEN="your_refresh_token"

curl -X POST "http://localhost:8081/refresh?refresh_token=${REFRESH_TOKEN}"
```
