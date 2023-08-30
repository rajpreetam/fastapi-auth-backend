from core.utils.custom_exceptions import InternalServerError
from sqlalchemy.orm import Session
from accounts.models import User


def get_user_by_email(email: str, db: Session):
    try:
        user = db.query(
            User.id,
            User.email
        ).filter(
            User.email == email
        ).one_or_none()
        if not user:
            return False
        return user
    except Exception as e:
        print(f'accounts.queries.regenerate_toke_query.get_user_by_email: {e}')
        db.rollback()
        raise InternalServerError
