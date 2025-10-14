from sqlmodel import Session
from app.core.database import engine
from app.seed.user import seed_default_first_superuser
from app.seed.tag import seed_default_tags


def seed_default_datas(*, session: Session):
    seed_default_first_superuser(session=session)
    seed_default_tags(session=session)
    print("✅ All Default datas seeded successfully.")


if __name__ == "__main__":
    with Session(engine) as session:
        seed_default_datas(session=session)
