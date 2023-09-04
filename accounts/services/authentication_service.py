from fastapi import status, Response
from core.utils.custom_exceptions import InternalServerError
from core.utils.custom_response import CustomResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from accounts.queries.authentication_query import get_user_by_email_password
from accounts.utils.jwt_utils import create_access_token, create_refresh_token
from core.settings import get_settings
from accounts.utils.cookie_utils import set_access_in_cookie, set_refresh_in_cookie

settings = get_settings()


def authentication_service(response: Response, db, data: OAuth2PasswordRequestForm):
    try:
        user = get_user_by_email_password(data.username, data.password, db)
        if not user:
            return CustomResponse(
                False,
                401,
                None,
                'Username or password is incorrect'
            ).json_response()
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        set_access_in_cookie(access_token, response)
        set_refresh_in_cookie(refresh_token, response)

        return_data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return CustomResponse(True, 201, return_data, 'Authenticated successfully')
    except Exception as e:
        print(f'accounts.services.authentication_service: {e}')
        raise InternalServerError
