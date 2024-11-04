"""Authentication router."""

from typing import Annotated, Any

from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from keycloak import KeycloakPostError
from loguru import logger
from pydantic import SecretStr

from py_event_planning.database.db import AsyncSessionDependency
from py_event_planning.features.auth import service as AuthService
from py_event_planning.features.auth.schemas import (
    AuthUserToken,
    RefreshToken,
    RegisterUserInput,
    Token,
    TokenResponse,
)
from py_event_planning.features.core.unit_of_work import sqlalchemy_uow
from py_event_planning.features.user.schemas import UserCreate, UserSchema

router = APIRouter()


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """Wrapper around OAuth2PasswordRequestForm to make password a SecretStr."""

    # TODO: grant_type, scope, client_id, client_secret?
    def __init__(self, username: str = Form(...), password: SecretStr = Form(...)):
        super().__init__(username=username, password=str(password.get_secret_value()))


@router.post(
    "/session/token/unsecured",
    description="Fetch all of the auth token(s) and information. (Only use for educational purposes.)",
)
async def login_unsecure(form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login user nd pass back all of the information."""
    try:
        token = await AuthService.authenticate_user(form_data.username, form_data.password)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post(
    "/session/token",
    description="Only fetch the information and the auth token(s) will be stored in an httpOnly cookie.",
)
async def login(
    response: Response,
    form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """Login user and only pass back the non-auth token information."""
    try:
        token = await AuthService.authenticate_user(form_data.username, form_data.password)
        response.set_cookie(key="access_token", value=token.access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=token.refresh_token, httponly=True)
        response.set_cookie(key="id_token", value=token.id_token, httponly=True)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post(
    "/session/refresh/unsecured",
    description="Refresh and return auth info and tokens together. (Only use for educational purposes).",
)
async def refresh_unsecured(token: RefreshToken) -> Token:
    """Refresh and return auth info and tokens together. (Only use for educational purposes)."""
    try:
        new_token = await AuthService.refresh_user_token(token.token)
        return new_token
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/session/refresh", description="Refresh tokens in cookies and return other auth info.")
async def refresh(
    current_user: AuthService.UserAuthOptional,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
) -> TokenResponse:
    """Refresh tokens in cookies and return other auth info."""
    try:
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
    except HTTPException as e:
        raise e
    except KeycloakPostError as e:
        logger.error("Failed to refresh token: {} - {}", e.response_code, e.response_body)
        if e.response_code == 400:
            logger.warning("Bad request - the refresh token may be expired or invalid.")
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            response.delete_cookie("id_token")
        elif e.response_code == 401:
            logger.error("Unauthorized - check client credentials or permissions.")
        else:
            logger.error("An unexpected error occurred while refreshing the token.")
        response.status_code = e.response_code
        response.body = e.response_body
        return response
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str) from e


@router.post("/session/logout")
async def logout_user(
    response: Response,
    current_user: AuthService.UserAuthOptional,
    # bearer_token: RefreshToken | None = None,
    refresh_token: str | None = Cookie(default=None),
) -> None:
    """Log the user out and clear auth cookies."""
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/user")
async def get_user(current_user: AuthService.UserAuth) -> AuthUserToken:
    """Fetch the user information.

    Args:
        current_user (AuthService.UserAuth): _description_

    Returns:
        _type_: _description_
    """
    try:
        logger.info(current_user)
        return current_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/user")
async def register_user(
    user: RegisterUserInput,
    db: AsyncSessionDependency,
) -> UserSchema:
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
        kc_user_id = await AuthService.create_keycloak_user(user)  # Register the user in Keycloak
        logger.info("Keycloak user created with id={}", kc_user_id)
        async with sqlalchemy_uow(db, None) as uow:
            create_input = UserCreate(id=str(kc_user_id).strip(), username=user.username)
            pg_user = await uow.user_repo.create(model_in=create_input, return_model=True)
            await uow.commit()
        return pg_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/user")
async def delete_user_endpoint(
    current_user: AuthService.UserAuth,
    db: AsyncSessionDependency,
) -> Any:
    """Delete an existing user."""
    try:
        logger.debug("Deleting user", extra=current_user)
        await AuthService.delete_user(current_user.preferred_username)
        async with sqlalchemy_uow(db, None) as uow:
            delete_res = await uow.user_repo.delete(entity_id=current_user.sub)
            if not delete_res:
                logger.warning("User not found!", extra={"entity_id": current_user.sub})
            await uow.commit()
        return current_user.sub
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
