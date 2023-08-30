from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from core.utils.custom_exceptions import InternalServerError
from accounts.schemas import (
    RegisterUserRequestModel,
    RegisterUserResponseModel,
    TokenResponseModel,
    RefreshRequestModel,
    VerifyTokenRequestModel
)
from core.database import db_dependency
from accounts.services.register_user_service import register_user_service
from accounts.services.authentication_service import authentication_service
from accounts.services.regenerate_token_service import regenerate_token_service
from core.utils.schemas.custom_response_schema import CustomResponseModel
from accounts.services.verify_token_service import verify_token_service

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Accounts']
)


@router.post('/register', response_model=RegisterUserResponseModel, status_code=201)
async def register_user_router(data: RegisterUserRequestModel, db: db_dependency):
    try:
        return register_user_service(db, data)
    except Exception as e:
        print(f'accounts.routers.register_user_router: {e}')
        raise InternalServerError


@router.post('/token', response_model=TokenResponseModel, status_code=201)
async def token_authentication_router(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    try:
        return authentication_service(db, data)
    except Exception as e:
        print(f'accounts.routers.register_user_router: {e}')
        raise InternalServerError


@router.post('/refresh', response_model=TokenResponseModel, status_code=201)
async def refresh_token_router(data: RefreshRequestModel, db: db_dependency):
    try:
        return regenerate_token_service(db, data)
    except Exception as e:
        print(f'accounts.routers.register_user_router: {e}')
        raise InternalServerError


@router.post('/verify', response_model=CustomResponseModel, status_code=200)
async def verify_token_router(data: VerifyTokenRequestModel, db: db_dependency):
    try:
        return verify_token_service(db, data)
    except Exception as e:
        print(f'accounts.routers.register_user_router: {e}')
        raise InternalServerError
