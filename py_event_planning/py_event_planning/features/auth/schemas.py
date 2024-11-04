"""Auth Models."""

from pydantic import BaseModel, Field, SecretStr


class RefreshToken(BaseModel):
    """Refresh token body (for unsecured routes not using httpOnly cookies)."""

    token: str


class TokenResponse(BaseModel):
    """Token Response for routes using httpOnly cookies."""

    # access_token: str
    expires_in: int
    refresh_expires_in: int
    # refresh_token: str
    token_type: str
    id_token: str
    not_before_policy: int = Field(..., alias="not-before-policy")
    session_state: str
    scope: str


class Token(TokenResponse):
    """Token Response for unsecured routes not using httpOnly cookies."""

    access_token: str
    refresh_token: str


class RegisterUserInput(BaseModel):
    """User creation fields."""

    username: str = Field(alias="userName")
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    password: SecretStr

    # @field_serializer("password")
    # def serialize_secret_str(self, s: SecretStr, _info) -> str:
    #     """Convert secret to string."""
    #     return s.get_secret_value()


class DeleteUserInput(BaseModel):
    """User deletion fields."""

    username: str


class AuthUserToken(BaseModel):
    """Fields that come back in the user's ID token."""

    exp: int
    iat: int
    jti: str
    iss: str
    aud: str
    sub: str
    typ: str
    azp: str
    sid: str
    at_hash: str
    acr: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str
