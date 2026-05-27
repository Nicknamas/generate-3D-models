from flask_jwt_extended import jwt_required, get_jwt_identity
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

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
@jwt_required()
def get_users():
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        list_user_get_dto = user_service.get_list()

    return [asdict(user) for user in list_user_get_dto]


@router.get('/users/<int:user_id>')
@jwt_required()
def get_user(user_id: int):
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        user = user_service.get_one_or_none(UserModel.id == user_id)
        if not user:
            return {"error": "User not found"}, 404
    return asdict(user)


@router.delete('/users/<int:user_id>')
@jwt_required()
def delete_user(user_id: int):
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)

        # Опционально: не даем удалить самого себя
        current_username = get_jwt_identity()
        current_user = user_repo.get_one_or_none(UserModel.username == current_username)
        if current_user and current_user.id == user_id:
            return {"error": "Cannot delete yourself"}, 400

        if user_service.delete_by_id(user_id):
            return {"msg": "User deleted successfully"}, 200
        else:
            return {"error": "User not found"}, 404
