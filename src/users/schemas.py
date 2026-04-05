from datetime import datetime
from typing import Annotated
import re
from pydantic import BaseModel, EmailStr, PositiveInt, ConfigDict, Field, field_validator, UUID4
from pydantic.types import StringConstraints


PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=32)]

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: PasswordStr
    age: PositiveInt | None = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r'[A-Z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'[0-9]', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return value


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    age: PositiveInt | None = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    age: PositiveInt | None = None
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginationParams(BaseModel):
    limit: int = Field(default=10, gt=0, le=100 ,description="Макс. количество записей для получения")
    offset: int = Field(default=0, ge=0, description="Смещение для пагинации")


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponseSchema(BaseModel):
    user: UserSchema
    access_token: str
    token_type: str = "bearer"
