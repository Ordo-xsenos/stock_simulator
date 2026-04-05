from pydantic import UUID4
from src.users.dependencies import PaginationDep, CurrentUserDep
from src.users.schemas import UserCreateSchema, UserUpdateSchema, UserLoginSchema, LoginResponseSchema

from fastapi import APIRouter
from src.users.dependencies import UserServiceDep
from src.users.schemas import UserSchema
from src.users.security import create_access_token

users_router = APIRouter(prefix="/api/v1", tags=["Пользователи"])


@users_router.post("/users/", summary="Создать пользователя", tags=["Пользователи"])
async def create_user(data: UserCreateSchema, service: UserServiceDep):
    new_user = await service.create(data)
    return UserSchema.model_validate(new_user)


@users_router.get("/users/", response_model=list[UserSchema], summary="Получить пользователей", tags=["Пользователи"])
async def get_users(service: UserServiceDep, pagination: PaginationDep):
    users = await service.get_all(pagination)
    return [UserSchema.model_validate(user) for user in users]

@users_router.put("/users/{user_id}", summary="Обновить пользователя", tags=["Пользователи"])
async def update_user(
        user_id: UUID4,
        data: UserUpdateSchema,
        service: UserServiceDep
):
    updated_user = await service.update(user_id, data)
    return UserSchema.model_validate(updated_user)


@users_router.delete("/users/{user_id}", summary="Удалить пользователя", tags=["Пользователи"])
async def delete_user(user_id: UUID4, service: UserServiceDep):
    await service.delete(user_id)
    return {"message": f"Пользователь с id {user_id} удалён"}


@users_router.post("/users/register", summary="Регистрация", tags=["Пользователи"])
async def register_user(data: UserCreateSchema, service: UserServiceDep):
    new_user = await service.create(data)
    return UserSchema.model_validate(new_user)

@users_router.post("/users/login", summary="Авторизация", tags=["Пользователи"])
async def login_user(data: UserLoginSchema, service: UserServiceDep) -> LoginResponseSchema:
    user = await service.authenticate(data)
    jwt_token = create_access_token(
        user.id,
    )

    return LoginResponseSchema(
        user=UserSchema.model_validate(user),
        access_token=jwt_token,
        token_type="bearer"
    )

@users_router.get("/users/me", summary="Получить информацию о текущем пользователе", tags=["Пользователи"])
async def get_user_profile(current_user: CurrentUserDep) -> UserSchema:
    return UserSchema.model_validate(current_user)