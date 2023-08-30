from accounts.schemas import RefreshRequestModel
from core.utils.custom_exceptions import InternalServerError
from jose import jwt
from core.settings import get_settings
from accounts.queries.regenerate_token_query import get_user_by_email
from core.utils.custom_response import CustomResponse
from accounts.utils.jwt_utils import create_access_token, create_refresh_token

settings = get_settings()


def regenerate_token_service(db, data: RefreshRequestModel):
    try:
        refresh = data.refresh
        payload = jwt.decode(refresh, settings.REFRESH_SECRET, algorithms=[settings.ALGORITHM])
        email = payload['sub']
        user = get_user_by_email(email, db)
        if user:
            return CustomResponse(
                True,
                201,
                {
                    'access': create_access_token(user.id, user.email),
                    'refresh': create_refresh_token(user.id, user.email)
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
            'Refresh token is invalid'
        ).json_response()

    except Exception as e:
        print(f'accounts.services.regenerate_token_service: {e}')
        raise InternalServerError
