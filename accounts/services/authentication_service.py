from fastapi import status
from core.utils.custom_exceptions import InternalServerError
from core.utils.custom_response import CustomResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from accounts.queries.authentication_query import get_user_by_email_password
from accounts.utils.jwt_utils import create_access_token, create_refresh_token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')


def authentication_service(db, data: OAuth2PasswordRequestForm):
    try:
        user = get_user_by_email_password(data.username, data.password, db)
        if not user:
            return CustomResponse(
                False,
                401,
                None,
                'Username or password is incorrect'
            ).json_response()
        access = create_access_token(user.id, user.email)
        refresh = create_refresh_token(user.id, user.email)
        return_data = {
            'access': access,
            'refresh': refresh
        }
        return CustomResponse(True, 201, return_data, 'Authenticated successfully')
    except Exception as e:
        print(f'accounts.services.authentication_service: {e}')
        raise InternalServerError
