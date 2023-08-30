from accounts.schemas import VerifyTokenRequestModel
from core.utils.custom_exceptions import InternalServerError
from core.utils.custom_response import CustomResponse
from jose import jwt
from core.settings import get_settings
from datetime import datetime

settings = get_settings()


def verify_token_service(db, data: VerifyTokenRequestModel):
    try:
        access = data.access
        payload = jwt.decode(access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload['exp']
        exp_time = datetime.fromtimestamp(exp)
        current_time = datetime.utcnow()
        if current_time < exp_time:
            return CustomResponse(True, 200, None, 'Token verified successfully')
        else:
            return CustomResponse(False, 403, None, 'Token is expired').json_response()

    except jwt.ExpiredSignatureError:
        return CustomResponse(
            False,
            403,
            None,
            'Access token is expired'
        ).json_response()

    except jwt.JWTError:
        return CustomResponse(
            False,
            403,
            None,
            'Access token is invalid'
        ).json_response()

    except Exception as e:
        print(f'accounts.services.verify_token_service: {e}')
        raise InternalServerError
