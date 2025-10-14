import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class RegisterResponse(UserResponse):
    pass


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class CurrentUserResponse(UserResponse):
    pass


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class LogoutSchema(BaseModel):
    refresh_token: str
