from sqlmodel import Session, select
from app.models.tag import Tag


def seed_default_tags(*, session: Session):
    default_tags = [
        {"name": "Development", "color_hex": "#3B82F6"},
        {"name": "Bug", "color_hex": "#EF4444"},
        {"name": "Modification", "color_hex": "#F59E0B"},
        {"name": "Research", "color_hex": "#10B981"},
        {"name": "Review", "color_hex": "#8B5CF6"},
    ]

    for tag_data in default_tags:
        existing_tag = session.exec(
            select(Tag).where(Tag.name == tag_data["name"])
        ).first()
        if not existing_tag:
            tag = Tag(**tag_data)
            session.add(tag)

    session.commit()
    print("✅ Default tags seeded successfully.")
