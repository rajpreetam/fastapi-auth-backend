from pydantic import BaseModel
from core.utils.schemas.custom_response_schema import CustomResponseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class RegisterUserRequestModel(UserBase):
    password: str
    confirm_password: str


class RegisterUserResponseData(UserBase):
    id: int


class RegisterUserResponseModel(CustomResponseModel):
    data: RegisterUserResponseData | None = None


class TokenData(BaseModel):
    access_token: str
    refresh_token: str


class TokenResponseModel(CustomResponseModel):
    data: TokenData


class RefreshRequestModel(BaseModel):
    refresh: str


class VerifyTokenRequestModel(BaseModel):
    access: str
