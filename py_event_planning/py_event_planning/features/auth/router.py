"""Authentication router."""

from typing import Annotated, Any

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from py_event_planning.features.auth import service as AuthService
from py_event_planning.features.auth.schemas import (
    AuthUserToken,
    RefreshToken,
    RegisterUserInput,
    Token,
    TokenResponse,
)

router = APIRouter()


@router.post(
    "/session/token/unsecured",
    description="Fetch all of the auth token(s) and information. (Only use for educational purposes.)",
)
async def login_unsecure(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login user nd pass back all of the information."""
    token = await AuthService.authenticate_user(form_data.username, form_data.password)
    return token


@router.post(
    "/session/token",
    description="Only fetch the information and the auth token(s) will be stored in an httpOnly cookie.",
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """Login user and only pass back the non-auth token information."""
    token = await AuthService.authenticate_user(form_data.username, form_data.password)
    response.set_cookie(key="access_token", value=token.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=token.refresh_token, httponly=True)
    response.set_cookie(key="id_token", value=token.id_token, httponly=True)
    return token


@router.post(
    "/session/refresh/unsecured",
    description="Refresh and return auth info and tokens together. (Only use for educational purposes).",
)
async def refresh_unsecured(token: RefreshToken) -> Token:
    """Refresh and return auth info and tokens together. (Only use for educational purposes)."""
    new_token = await AuthService.refresh_user_token(token.token)
    return new_token


@router.post("/session/refresh", description="Refresh tokens in cookies and return other auth info.")
async def refresh(
    current_user: AuthService.UserAuthOptional,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
) -> TokenResponse:
    """Refresh tokens in cookies and return other auth info."""
    user = {}
    if current_user:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
    with logger.contextualize(user=user, log_threads=True):
        if not refresh_token:
            err_msg = "No refresh_token cookie found!"
            logger.info(err_msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=err_msg)
        logger.info("Refreshing token!")
        new_token = await AuthService.refresh_user_token(refresh_token)
        response.set_cookie(key="access_token", value=new_token.access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=new_token.refresh_token, httponly=True)
        response.set_cookie(key="id_token", value=new_token.id_token, httponly=True)
        return new_token


@router.post("/session/logout")
async def logout_user(
    response: Response,
    current_user: AuthService.UserAuthOptional,
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
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("id_token")
        return response
    user = {}
    if current_user:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
    with logger.contextualize(user=user, log_threads=True):
        await AuthService.logout(token)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("id_token")


@router.get("/user")
async def get_user(current_user: AuthService.UserAuth) -> AuthUserToken:
    """Fetch the user information.

    Args:
        current_user (AuthService.UserAuth): _description_

    Returns:
        _type_: _description_
    """
    logger.info(current_user)
    return current_user


@router.post("/user")
async def register_user(user: RegisterUserInput) -> Any:
    """Create a new user (register).

    Args:
        user (RegisterUserInput): _description_

    Raises:
        e: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        return await AuthService.create_keycloak_user(user)  # Register the user in Keycloak
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/user")
async def delete_user_endpoint(current_user: AuthService.UserAuth) -> Any:
    """Delete an existing user."""
    try:
        username = current_user.get("preferred_username")
        logger.debug("Deleting user", extra=current_user)
        return await AuthService.delete_user(username)  # Delete the user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
