from typing import Annotated, Optional
from fastapi import Depends, Request
from jose import jwt
from core.settings import get_settings
from core.utils.custom_exceptions import InternalServerError
from fastapi.exceptions import HTTPException

settings = get_settings()


class CustomAuthentication:
    def __init__(self):
        pass

    def __call__(self, request: Request) -> Optional[str]:
        access_token = request.cookies.get('access_token')
        if not access_token:
            return ''
        return access_token


manager = CustomAuthentication()


async def get_current_user(access: Annotated[str, Depends(manager)]):
    try:
        payload = jwt.decode(access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload['sub']
        user_id = payload['id']
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not verify user')
        return {'email': email, 'id': user_id}

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Token is invalid or expired')

    except Exception as e:
        print(f'accounts.auth.get_current_user: {e}')
        raise InternalServerError

user_dependency = Annotated[dict, Depends(get_current_user)]
