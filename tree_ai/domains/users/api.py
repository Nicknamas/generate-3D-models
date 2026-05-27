from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.core.exceptions import UserNotFound
from tree_ai.domains.users.models import UserModel
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.schemas import UserCreate
from tree_ai.domains.users.services import UserService


router = Blueprint("users", __name__)


@router.post('/users')
def create_user():
    data: dict[str, Any] = request.get_json()
    user_dto = UserCreate(**data)

    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        user_get_dto = user_service.create(user_dto)

    return asdict(user_get_dto)


@router.get('/users')
def get_users():
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        list_user_get_dto = user_service.get_list()

    return [asdict(user_get_dto) for user_get_dto in list_user_get_dto]


@router.get('/users/<int:user_id>')
def get_user(user_id: int):
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        user = user_service.get_one_or_none(UserModel.id == user_id)

    return asdict(user)
