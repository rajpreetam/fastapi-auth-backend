from core.utils.custom_exceptions import InternalServerError
from sqlalchemy.orm import Session
from accounts.models import User
from accounts.utils.password_util import verify_password


def get_user_by_email_password(email: str, password: str, db: Session):
    try:
        user = db.query(
            User.id,
            User.email,
            User.password
        ).filter(
            User.email == email
        ).one_or_none()
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        print(f'accounts.queries.authentication_query.get_user_by_email_password: {e}')
        db.rollback()
        raise InternalServerError
