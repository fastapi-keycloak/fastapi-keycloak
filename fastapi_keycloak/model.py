from enum import Enum

from pydantic import BaseModel, Field, SecretStr

from fastapi_keycloak.exceptions import KeycloakError


class HTTPMethod(Enum):
    """Represents the basic HTTP verbs

    Values:
        - GET: get
        - POST: post
        - DELETE: delete
        - PUT: put
    """

    GET = "get"
    POST = "post"
    DELETE = "delete"
    PUT = "put"


class KeycloakUser(BaseModel):
    """Represents a user object of Keycloak.

    Attributes:
        id (str):
        createdTimestamp (int):
        username (str):
        enabled (bool):
        totp (bool):
        emailVerified (bool):
        firstName (Optional[str]):
        lastName (Optional[str]):
        email (Optional[str]):
        disableableCredentialTypes (List[str]):
        requiredActions (List[str]):
        realmRoles (List[str]):
        notBefore (int):
        access (dict):
        attributes (Optional[dict]):

    Notes: Check the Keycloak documentation at https://www.keycloak.org/docs-api/15.0/rest-api/index.html for
    details. This is a mere proxy object.
    """

    id: str
    createdTimestamp: int
    username: str
    enabled: bool
    totp: bool
    emailVerified: bool
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    disableableCredentialTypes: list[str]
    requiredActions: list[str]
    realmRoles: list[str] | None = None
    notBefore: int
    access: dict | None = None
    attributes: dict | None = None


class UsernamePassword(BaseModel):
    """Represents a request body that contains username and password

    Attributes:
        username (str): Username
        password (str): Password, masked by swagger
    """

    username: str
    password: SecretStr


class OIDCUser(BaseModel):
    """Represents a user object of Keycloak, parsed from access token

    Attributes:
        sub (str):
        iat (int):
        exp (int):
        scope (str):
        email_verified (bool):
        name (Optional[str]):
        given_name (Optional[str]):
        family_name (Optional[str]):
        email (Optional[str]):
        preferred_username (Optional[str]):
        realm_access (dict):
        resource_access (dict):
        extra_fields (dict):

    Notes: Check the Keycloak documentation at https://www.keycloak.org/docs-api/15.0/rest-api/index.html for
    details. This is a mere proxy object.
    """

    azp: str | None = None
    sub: str
    iat: int
    exp: int
    scope: str | None = None
    email_verified: bool
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    email: str | None = None
    preferred_username: str | None = None
    realm_access: dict | None = None
    resource_access: dict | None = None
    extra_fields: dict = Field(default_factory=dict)

    @property
    def roles(self) -> list[str]:
        """Returns the roles of the user

        Returns:
            List[str]: If the realm access dict contains roles
        """
        if not self.realm_access and not self.resource_access:
            raise KeycloakError(
                status_code=404,
                reason="The 'realm_access' and 'resource_access' sections of the provided access token are missing.",
            )
        roles = []
        if self.realm_access:
            if "roles" in self.realm_access:
                roles += self.realm_access["roles"]
        if self.azp and self.resource_access:
            if self.azp in self.resource_access:
                if "roles" in self.resource_access[self.azp]:
                    roles += self.resource_access[self.azp]["roles"]
        if not roles:
            raise KeycloakError(
                status_code=404,
                reason="The 'realm_access' and 'resource_access' sections of the provided access token did not "
                "contain any 'roles'",
            )
        return roles

    def __str__(self) -> str:
        """String representation of an OIDCUser"""
        return self.preferred_username


class KeycloakIdentityProvider(BaseModel):
    """Keycloak representation of an identity provider

    Attributes:
        alias (str):
        internalId (str):
        providerId (str):
        enabled (bool):
        updateProfileFirstLoginMode (str):
        trustEmail (bool):
        storeToken (bool):
        addReadTokenRoleOnCreate (bool):
        authenticateByDefault (bool):
        linkOnly (bool):
        firstBrokerLoginFlowAlias (str):
        config (dict):

    Notes: Check the Keycloak documentation at https://www.keycloak.org/docs-api/15.0/rest-api/index.html for
    details. This is a mere proxy object.
    """

    alias: str
    internalId: str
    providerId: str
    enabled: bool
    updateProfileFirstLoginMode: str
    trustEmail: bool
    storeToken: bool
    addReadTokenRoleOnCreate: bool
    authenticateByDefault: bool
    linkOnly: bool
    firstBrokerLoginFlowAlias: str
    config: dict


class KeycloakRole(BaseModel):
    """Keycloak representation of a role

    Attributes:
        id (str):
        name (str):
        composite (bool):
        clientRole (bool):
        containerId (str):

    Notes: Check the Keycloak documentation at https://www.keycloak.org/docs-api/15.0/rest-api/index.html for
    details. This is a mere proxy object.
    """

    id: str
    name: str
    composite: bool
    clientRole: bool
    containerId: str


class KeycloakToken(BaseModel):
    """Keycloak representation of a token object

    Attributes:
        access_token (str): An access token
        refresh_token (str): An a refresh token, default None
        id_token (str): An issued by the Authorization Server token id, default None
    """

    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None

    def __str__(self):
        """String representation of KeycloakToken"""
        return f"Bearer {self.access_token}"


class KeycloakGroup(BaseModel):
    """Keycloak representation of a group

    Attributes:
        id (str):
        name (str):
        path (Optional[str]):
        realmRoles (Optional[str]):
    """

    id: str
    name: str
    path: str | None = None
    realmRoles: list[str] | None = None
    subGroups: list["KeycloakGroup"] | None = None


KeycloakGroup.update_forward_refs()
