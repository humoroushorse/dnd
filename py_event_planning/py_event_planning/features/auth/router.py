"""Authentication router."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from py_event_planning.features.auth import service as AuthService
from py_event_planning.features.auth.models import RefreshToken, Token, TokenResponse

router = APIRouter()


@router.post(
    "/token/unsecured",
    description="Fetch all of the auth token(s) and information. (Only use for educational purposes.)",
)
async def login_unsecure(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login user nd pass back all of the information."""
    token = await AuthService.authenticate_user(form_data.username, form_data.password)
    return token


@router.post(
    "/token", description="Only fetch the information and the auth token(s) will be stored in an httpOnly cookie."
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """Login user and only pass back the non-auth token information."""
    token = await AuthService.authenticate_user(form_data.username, form_data.password)
    response.set_cookie(key="access_token", value=token.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=token.refresh_token, httponly=True)
    return token


@router.post(
    "/refresh/unsecured",
    description="Refresh and return auth info and tokens together. (Only use for educational purposes).",
)
async def refresh_unsecured(token: RefreshToken) -> Token:
    """Refresh and return auth info and tokens together. (Only use for educational purposes)."""
    new_token = await AuthService.refresh_token(token.token)
    return new_token


@router.post("/refresh", description="Refresh tokens in cookies and return other auth info.")
async def refresh(response: Response, refresh_token: str | None = Cookie(default=None)) -> TokenResponse:
    """Refresh tokens in cookies and return other auth info."""
    if not refresh_token:
        err_msg = "No refresh_token cookie found!"
        logger.info(err_msg)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=err_msg)
    new_token = await AuthService.refresh_token(refresh_token)
    response.set_cookie(key="access_token", value=new_token.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=new_token.refresh_token, httponly=True)
    return new_token


@router.post("/logout")
async def logout_user(
    response: Response,
    # bearer_token: RefreshToken | None = None,
    refresh_token: str | None = Cookie(default=None),
) -> None:
    """Log the user out and clear auth cookies."""
    token: str | None = refresh_token
    # if not token:
    #     token = bearer_token.token if bearer_token else None
    if not token:
        err_msg = "No refresh_token cookie found to delete (in request body or cookie)!"
        logger.info(err_msg)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=err_msg)
    await AuthService.logout(token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.get("/user")
async def get_user(current_user: AuthService.UserAuth) -> dict:
    """Fetch the user information.

    Args:
        current_user (AuthService.UserAuth): _description_

    Returns:
        _type_: _description_
    """
    logger.info(current_user)
    return current_user
