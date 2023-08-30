from accounts.schemas import RegisterUserRequestModel
from core.utils.custom_exceptions import InternalServerError
from sqlalchemy.orm import Session
from accounts.models import User
from accounts.utils.password_util import hash_password


def register_user_query(db: Session, data: RegisterUserRequestModel):
    try:
        del data.confirm_password
        data.password = hash_password(data.password)
        user = User(**data.model_dump())
        db.add(user)
        db.commit()
        return user
    except Exception as e:
        print(f'accounts.queries.register_user_query: {e}')
        db.rollback()
        raise InternalServerError


def find_user_by_email(db: Session, email: str) -> bool:
    try:
        user = db.query(User.email).filter_by(email=email).first()
        if user:
            return True
        return False
    except Exception as e:
        print(f'accounts.queries.find_user_by_email: {e}')
        db.rollback()
        raise InternalServerError
