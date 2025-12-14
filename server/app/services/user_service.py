from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_new_user(*, session: Session, user_create: UserCreate) -> User:
    user_obj = User.model_validate(
        user_create,
        update={
            "hashed_password": get_password_hash(password=user_create.password),
            "image_url": f"https://api.dicebear.com/9.x/adventurer/svg?seed={user_create.full_name}"
        }
    )
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj


def authenticate_user(*, session: Session, email: str, password: str) -> User:
    user = get_user_by_email(session=session, email=email)
    if user and not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user
