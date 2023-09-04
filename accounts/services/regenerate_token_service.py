from fastapi import Response, Request
from core.utils.custom_exceptions import InternalServerError
from jose import jwt
from core.settings import get_settings
from accounts.queries.regenerate_token_query import get_user_by_email
from core.utils.custom_response import CustomResponse
from accounts.utils.jwt_utils import create_access_token, create_refresh_token
from accounts.utils.cookie_utils import set_access_in_cookie, set_refresh_in_cookie

settings = get_settings()


def regenerate_token_service(request: Request, response: Response, db):
    try:
        refresh = request.cookies.get('refresh_token') or ''

        payload = jwt.decode(refresh, settings.REFRESH_SECRET, algorithms=[settings.ALGORITHM])
        email = payload['sub']
        user = get_user_by_email(email, db)
        if user:
            access_token = create_access_token(user.id, user.email)
            refresh_token = create_refresh_token(user.id, user.email)

            set_access_in_cookie(access_token, response)
            set_refresh_in_cookie(refresh_token, response)

            return CustomResponse(
                True,
                201,
                {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                'Token refreshed successfully'
            )
    except jwt.ExpiredSignatureError:
        return CustomResponse(
            False,
            403,
            None,
            'Refresh token is expired'
        ).json_response()

    except jwt.JWTError:
        return CustomResponse(
            False,
            403,
            None,
            'Refresh token is invalid or expired'
        ).json_response()

    except Exception as e:
        print(f'accounts.services.regenerate_token_service: {e}')
        raise InternalServerError
