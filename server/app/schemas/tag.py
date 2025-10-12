import uuid
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    color_hex: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: uuid.UUID
