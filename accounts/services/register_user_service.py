from fastapi import status
from accounts.schemas import RegisterUserRequestModel
from core.utils.custom_exceptions import InternalServerError
from core.utils.custom_response import CustomResponse
from accounts.queries.register_user_query import register_user_query, find_user_by_email


def register_user_service(db, data: RegisterUserRequestModel):
    try:
        if len(data.password) < 8:
            return CustomResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                'Password must be 8 or more characters long'
            ).json_response()

        if data.password != data.confirm_password:
            return CustomResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                'Password did not matched'
            ).json_response()

        if find_user_by_email(db, data.email):
            return CustomResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                'User with this email already exists'
            ).json_response()

        user = register_user_query(db, data)
        return CustomResponse(True, 201, user, 'User created successfully')
    except Exception as e:
        print(f'accounts.services.register_user_service: {e}')
        raise InternalServerError
