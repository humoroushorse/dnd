"""Module used for keycloak backend calls."""

import time
from functools import lru_cache
from typing import Annotated

import aiohttp
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from keycloak.keycloak_openid import KeycloakOpenID
from loguru import logger

from py_dnd.core.config import Settings, get_settings
from py_dnd.features.auth.schemas import AuthUserToken, RegisterUserInput, Token

settings: Settings = get_settings()

# This is just for the FastAPI docs
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    # example authorizationUrl: https://sso.example.com/auth/
    authorizationUrl=settings.KEYCLOAK_SERVER_URL,
    # example tokenUrl: https://sso.example.com/auth/realms/example-realm/protocol/openid-connect/token
    tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM_NAME}/protocol/openid-connect/token",
    scopes={"openid": "Basic information"},
)

# This is just for the FastAPI docs (allow logging in with user/pass in docs)
#    TODO: I don't think swagger can do refresh tokens... look into it though
# oauth2_scheme2 = OAuth2PasswordBearer(
#     tokenUrl="/auth/session/token",
# )

# This actually does the auth checks
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,  # https://sso.example.com/auth/
    realm_name=settings.KEYCLOAK_REALM_NAME,  # example-realm
    client_id=settings.KEYCLOAK_CLIENT_ID,  # backend-client-id
    # client_secret_key=settings.KEYCLOAK_CLIENT_SECRET_KEY,  # your backend client secret
    verify=True,
)

# Configure the Keycloak admin client
keycloak_admin = KeycloakAdmin(
    server_url=f"{settings.KEYCLOAK_SERVER_URL}/auth",
    realm_name="master",  # default anyways
    client_id="admin-cli",  # default anyways
    username=settings.KEYCLOAK_ADMIN_USERNAME,
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    # user_realm_name="ttrpg",  # Target realm where users are added
)


# async def get_idp_public_key():
#     return (
#         "-----BEGIN PUBLIC KEY-----\n"
#         f"{keycloak_openid.public_key()}"
#         "\n-----END PUBLIC KEY-----"
#     )


async def get_auth(
    # refresh_token: str | None = Cookie(default=None),
    access_token: str | None = Cookie(default=None),
    id_token: str | None = Cookie(default=None),
    # force swagger to have the security scheme
    # _: Any = Security(oauth2_scheme2, use_cache=False),
) -> AuthUserToken:
    """Validate the user's access token and return it decoded.

    Args:
        access_token (str | None, optional): _description_. Defaults to Cookie(default=None).
        _ (Any, optional): _description_. Defaults to Security(oauth2_scheme2, use_cache=False).

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    if not access_token:
        err_msg = "No access_token cookie found!"
        logger.error(err_msg)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=err_msg)
    # public_key = await get_idp_public_key()
    try:
        decoded_access_token = keycloak_openid.decode_token(access_token)
        if "exp" not in decoded_access_token or decoded_access_token["exp"] < time.time():
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        # if 'aud' not in decoded_token or decoded_token['aud'] != 'expected-audience':
        #     raise HTTPException(status_code=401, detail="Invalid audience")
        decoded_id_token = keycloak_openid.decode_token(id_token)

        return AuthUserToken(**decoded_id_token)

    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


async def get_auth_optional(
    id_token: str | None = Cookie(default=None),
) -> AuthUserToken | None:
    """Validate the user's ID token if present and return it decoded.

    Args:
        id_token (str | None, optional): _description_. Defaults to Cookie(default=None).
        _ (Any, optional): _description_. Defaults to Security(oauth2_scheme2, use_cache=False).

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    if not id_token:
        return None
    try:
        decoded_id_token = keycloak_openid.decode_token(id_token, validate=False)
        return AuthUserToken(**decoded_id_token)
    except Exception as e:
        # TODO: make 401 ?
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# TODO: stonger typing on what's returned?
UserAuth = Annotated[AuthUserToken, Depends(get_auth)]
UserAuthOptional = Annotated[AuthUserToken | None, Depends(get_auth_optional)]


# KEYCLOAK_PUBLIC_KEY: str | None = \
#     "-----BEGIN PUBLIC KEY-----\n" f"{keycloak_openid.public_key()}" "\n-----END PUBLIC KEY-----"


# Fetch the public key from Keycloak
@lru_cache
async def get_keycloak_public_key() -> str:
    """Get the keycloak public key.

    Returns:
        _type_: _description_
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.KEYCLOAK_SERVER_URL}/auth/realms/{settings.KEYCLOAK_REALM_NAME}/protocol/openid-connect"
        ) as resp:
            resp.raise_for_status()
            jwks_uri = await resp.json()["jwks_uri"]
        async with session.get(jwks_uri) as resp:
            resp.raise_for_status()
            jwks = await resp.json()
        # TODO: may want to handle multiple keys differently...
        KEYCLOAK_PUBLIC_KEY = jwks["keys"][0]["x5c"][0]
    return f"-----BEGIN PUBLIC KEY-----\n{KEYCLOAK_PUBLIC_KEY}\n-----END PUBLIC KEY-----"


async def authenticate_user(username: str, password: str) -> Token:
    """Authenticate user with Keycloak backend.

    Args:
        username (str): _description_
        password (str): _description_

    Raises:
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    try:
        token = keycloak_openid.token(username, password)
        return Token(**token)
    except KeycloakAuthenticationError as error:
        raise HTTPException(status_code=401, detail="Invalid credentials") from error


# def verify_permission(required_roles: list | None = None) -> Callable[[str], Coroutine[Any, Any, Token]]:
#     """Verify user permissions.

#     Args:
#         required_roles (list | None, optional): _description_. Defaults to None.

#     Returns:
#         Callable[[str], Coroutine[Any, Any, Token]]: _description_
#     """

#     async def verify_token(token: str = Depends(oauth2_scheme)) -> Token:
#         """Verify token with Keycloak public key.

#         Args:
#             token: access token to decode

#         Returns:
#             Token decoded
#         """
#         try:
#             token_info = keycloak_openid.decode_token(
#                 token,
#                 key=await get_keycloak_public_key(),
#                 options={"verify_signature": True, "verify_aud": False, "exp": True},
#             )
#             resource_access = token_info["resource_access"]
#             app_name = settings.KEYCLOAK_CLIENT_ID
#             app_property = resource_access[app_name] if app_name in resource_access else {}
#             user_roles = app_property["roles"] if "roles" in app_property else []

#             if required_roles:
#                 for role in required_roles:
#                     if role not in user_roles:
#                         raise HTTPException(
#                             status_code=status.HTTP_403_FORBIDDEN,
#                             detail=f'Role "{role}" is required to perform this action',
#                         )

#             return Token(**token_info)
#         except (KeycloakGetError, JWTError) as error:
#             raise HTTPException(status_code=401, detail=str(error), headers={"WWW-Authenticate": "Bearer"}) from error

#     return verify_token


# async def verify_token(token: str = Depends(oauth2_scheme)) -> Token:
#     """Verify token with Keycloak public key.

#     Args:
#         token: access token to decode

#     Returns:
#         Token decoded
#     """
#     try:
#         decoded = keycloak_openid.decode_token(
#             token,
#             key=await get_keycloak_public_key(),
#             options={"verify_signature": True, "verify_aud": False, "exp": True},
#         )
#         return Token(**decoded)
#     except (KeycloakGetError, JWTError) as error:
#         raise HTTPException(status_code=401, detail=str(error), headers={"WWW-Authenticate": "Bearer"}) from error


async def refresh_user_token(token: str) -> Token:
    """Refresh the user's tokens.

    Args:
        token (str): _description_

    Raises:
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    try:
        return Token(**keycloak_openid.refresh_token(token))
    except KeycloakGetError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


async def logout(token: str) -> None:
    """Log the user out.

    Args:
        token (str): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        return keycloak_openid.logout(token)
    except KeycloakGetError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


async def create_keycloak_user(user: RegisterUserInput) -> str:
    """Create a new user in Keycloak."""
    # token = await get_admin_token()
    # # url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    # url = f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM_NAME}/users"
    # headers = {
    #     # "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }
    user_data = {
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "enabled": True,
        "credentials": [{"type": "password", "value": user.password.get_secret_value(), "temporary": False}],
    }
    logger.debug("Creating user with info: {}", {**user.model_dump(exclude={"paassword"}), "paassword": "REDACTED"})

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, json=user_data, headers=headers) as resp:
    #         resp.raise_for_status()
    #         status = resp.status
    #         if status != 201:
    #             logger.error("Failed to create user")
    #             raise HTTPException(status_code=status, detail="Failed to create user")
    #         return {"message": "User created successfully"}
    new_user = keycloak_admin.create_user(user_data)
    logger.debug("Created new user with id {}", new_user)
    return new_user


async def delete_user(username: str) -> None:
    """Remove user from Keycloak."""
    # token = await get_admin_token()
    # # url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users/{user_id}"
    # url = f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM_NAME}/users/{user_id}"

    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }

    # async with aiohttp.ClientSession() as session:
    #     async with session.delete(url, headers=headers) as resp:
    #         resp.raise_for_status()
    #         status = resp.status
    #         if status != 204:
    #             logger.error("Failed to delete user")
    #             raise HTTPException(status_code=status, detail="Failed to delete user")
    #         return {"message": "User deleted successfully"}

    users = keycloak_admin.get_users({"username": username})
    if not users:
        logger.warning("No users found with username: {}", username)
        return None
    logger.debug("Deleting first user from {}", [user["id"] for user in users])
    keycloak_admin.delete_user(user_id=users[0]["id"])


async def get_admin_token() -> str:
    """Get admin token for service functions like creating users."""
    # token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM_NAME}/protocol/openid-connect/token"
    token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        # "client_id": keycloak_openid.client_id,
        "client_id": "admin-cli",
        "username": settings.KEYCLOAK_ADMIN_USERNAME,
        "password": settings.KEYCLOAK_ADMIN_PASSWORD,
        # "client_secret": keycloak_openid.client_secret_key
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data=data, headers=headers) as resp:
            resp.raise_for_status()
            status = resp.status
            if status != 200:
                logger.error("Failed to delete user")
                raise HTTPException(status_code=status, detail="Failed to retrieve access token")
            resp_json = await resp.json()
            return resp_json.get("access_token")
