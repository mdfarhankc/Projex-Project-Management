from sqlmodel import Session, select
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


def seed_default_first_superuser(*, session: Session):
    existing_user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not existing_user:
        user = User(
            full_name=settings.FIRST_SUPERUSER_NAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(password=settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        session.add(user)

    session.commit()
    print("✅ Default super user seeded successfully.")
