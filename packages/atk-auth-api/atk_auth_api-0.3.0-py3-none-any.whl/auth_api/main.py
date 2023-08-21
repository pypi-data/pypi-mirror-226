import logging
import os
from typing import Annotated

from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import jwt
from jwt import PyJWKClient
from pydantic import BaseModel
import sentry_sdk

from .config import read_config_file, fetch_openid_config
from .oauth2_client import OAuth2Client


class ErrorResponse(BaseModel):
    error: str
    details: str | None


logging.basicConfig(level=logging.INFO)

config = read_config_file(path=os.environ.get("CONFIG_FILE", "./config.yaml"))
dex_config = fetch_openid_config(config.oidc.url)


if (sentry_dsn := os.environ.get("SENTRY_DSN")) is not None:
    sentry_sdk.init(sentry_dsn)
    logging.info("Sentry enabled")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
)

oauth2_client = OAuth2Client(
    oidc_config=config.oidc,
    dex_config=dex_config,
    redirect_uri=f"{config.api.url.rstrip('/')}/auth/v1/callback",
)


@app.get("/v1/login")
def v1_login() -> str:
    secure = config.api.url.startswith("https")
    login_url, state = oauth2_client.authorization_url(
        scope=["openid", "email", "profile"]
    )

    response = RedirectResponse(login_url)
    response.set_cookie(
        "original_state",
        value=state,
        max_age=60 * 5,
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    return response


@app.get("/v1/callback")
def v1_callback(
    response: Response,
    code: str,
    state: str,
    original_state: Annotated[str | None, Cookie()] = None,
):
    secure = config.api.url.startswith("https")
    if original_state is None:
        response.status_code = 400
        return "Missing original_state cookie"
    if original_state != state:
        response.status_code = 400
        return "Invalid state"
    response.delete_cookie("original_state")
    token = oauth2_client.fetch_token(code, state)
    response.set_cookie(
        "token",
        value=token["access_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    response.set_cookie(
        "access_token",
        value=token["access_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    response.set_cookie(
        "id_token",
        value=token["id_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )


@app.get("/v1/token")
def v1_token(response: Response, access_token: Annotated[str | None, Cookie()] = None):
    if access_token is None:
        response.status_code = 401
        return "Missing access_token cookie"
    return access_token


@app.get("/v1/userinfo")
def v1_userinfo(
    response: Response, access_token: Annotated[str | None, Cookie()] = None
):
    if access_token is None:
        response.status_code = 401
        return "Missing access_token cookie"
    user_info = oauth2_client.fetch_user_info({"access_token": access_token})
    return user_info


class UserResponse(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: int
    iat: int
    at_hash: str
    c_hash: str
    email: str
    email_verified: bool
    name: str
    preferred_username: str


@app.get("/v1/user")
def v1_user(
    response: Response,
    id_token: str,
) -> UserResponse | ErrorResponse:
    url = dex_config.jwks_uri
    jwk_client = PyJWKClient(url)
    signing_key = jwk_client.get_signing_key_from_jwt(id_token)
    try:
        data = jwt.decode(
            jwt=id_token,
            key=signing_key.key,
            algorithms=["RS256"],
            options={
                "verify_signature": True,
                "require": [
                    "aud",
                    "iss",
                    "exp",
                    "iat",
                ],
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_iat": True,
                "strict_aud": True,
            },
            audience=config.oidc.client_id,
            issuer=dex_config.issuer,
        )
    except jwt.exceptions.InvalidTokenError as e:
        response.status_code = 401
        logging.error(e)
        return {"error": "Invalid token", "details": str(e)}
    except Exception as e:
        response.status_code = 500
        logging.error(e)
        return {"error": "Internal server error"}
    if not data.get("email_verified"):
        response.status_code = 401
        return {"error": "Email not verified", "details": "Email not verified"}
    return UserResponse(**data)
