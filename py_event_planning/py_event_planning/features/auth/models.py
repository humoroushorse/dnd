"""Auth Models."""

from pydantic import BaseModel, Field


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
