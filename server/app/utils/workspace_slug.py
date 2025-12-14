from sqlmodel import Session, select
from app.utils.text import slugify

from app.models.workspace import Workspace


def generate_unique_workspace_slug(*, session: Session, base_name: str) -> str:
    """Generate a unique slug for workspace names."""
    base_slug = slugify(base_name)
    slug = base_slug
    counter = 1

    while session.exec(select(Workspace).where(Workspace.slug == slug)).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
