from fastapi import HTTPException
from pydantic import UUID4


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: UUID4):
        super().__init__(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )

class EmailAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Email already exists"
        )

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid email or password"
        )

class UserInactiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="User account is inactive"
        )

class TokenExpiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid token or token malformed",
            headers={"WWW-Authenticate": "Bearer"}
        )