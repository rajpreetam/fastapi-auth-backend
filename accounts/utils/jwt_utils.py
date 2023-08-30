from datetime import datetime, timedelta
from jose import jwt
from core.settings import get_settings

settings = get_settings()


def create_access_token(user_id: int, email: str):
    payload = {
        'sub': email,
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(days=0, minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(user_id: int, email: str):
    payload = {
        'sub': email,
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.REFRESH_SECRET, algorithm=settings.ALGORITHM)
