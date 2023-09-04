from fastapi import Response
from core.settings import get_settings

settings = get_settings()


def set_access_in_cookie(access_token: str, response: Response):
    response.set_cookie(
        key='access_token',
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRY_MINUTES * 60,
        path=settings.AUTH_COOKIE_PATH,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY == 'True',
        secure=settings.AUTH_COOKIE_SECURE == 'True',
        samesite=settings.AUTH_COOKIE_SAME_SITE
    )


def set_refresh_in_cookie(refresh_token: str, response: Response):
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRY_DAYS * 24 * 60 * 60,
        path=settings.AUTH_COOKIE_PATH,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY == 'True',
        secure=settings.AUTH_COOKIE_SECURE == 'True',
        samesite=settings.AUTH_COOKIE_SAME_SITE
    )
