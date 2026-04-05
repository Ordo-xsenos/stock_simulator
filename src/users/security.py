import uuid
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pydantic import UUID4

from src.config import settings
from src.users.exceptions import TokenExpiredError, InvalidTokenError

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: UUID4, scopes: list[str] = None) -> str:
    """Создает JWT токен для аутентификации пользователя.
    Включает в себя стандартные поля (sub, exp, iat, iss,
    aud) и уникальный jti для возможности отзыва токена.
    """
    actual_scopes = scopes if scopes is not None else ["read:users"] # по умолчанию только права на чтение
    now = datetime.now(timezone.utc)
    expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60

    payload = {
        "sub": str(user_id),
        "exp": now + timedelta(seconds=expires_in),
        "iat": now,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "jti": uuid.uuid4().hex, # Уникальный идентификатор токена для отзыва
        "scope": " ".join(actual_scopes) # Права доступа, можно расширить по необходимости
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"require": ["exp", "iat", "sub", "aud", "iss"]} # гарантируем наличие обязательных полей в токене
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()