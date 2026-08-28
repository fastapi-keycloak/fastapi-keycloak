from fastapi_keycloak.model import KeycloakToken, KeycloakUser, OIDCUser

TEST_PASSWORD = "test-password"


class TestAuthOnly:
    def test_auth_only_class_validates_tokens_from_the_admin_class(self, idp, idp_auth):
        """A FastAPIKeycloakAuth instance (no admin secret) must be able to validate/decode tokens for
        users that were created and logged in through a FastAPIKeycloak (admin) instance for the same
        realm/client — that's the whole point of splitting the two classes."""
        user: KeycloakUser = idp.create_user(
            first_name="test",
            last_name="user",
            username="auth_only_user@code-specialist.com",
            email="auth_only_user@code-specialist.com",
            password=TEST_PASSWORD,
            enabled=True,
            send_email_verification=False,
        )
        try:
            token: KeycloakToken = idp.user_login(username=user.username, password=TEST_PASSWORD)

            assert idp_auth.token_is_valid(token.access_token)

            current_user_function = idp_auth.get_current_user()
            current_user: OIDCUser = current_user_function(token=token.access_token)
            assert current_user.sub == user.id
        finally:
            idp.delete_user(user_id=user.id)

    def test_auth_only_class_has_no_admin_surface(self, idp_auth):
        assert not hasattr(idp_auth, "admin_token")
        assert not hasattr(idp_auth, "proxy")
        assert not hasattr(idp_auth, "create_user")
