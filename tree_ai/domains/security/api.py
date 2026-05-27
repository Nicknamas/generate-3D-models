from sqlalchemy import engine
from sqlalchemy.orm import Session
from typing import Any
from flask import Blueprint, request, jsonify

from tree_ai.core.exceptions import EmptyEmailException, EmptyPasswordException, IncorrectEmailOrUsernameException
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.services import UserService


router = Blueprint("security", __name__)


@router.post('/login')
def login():
    data: dict[str, Any] = request.get_json()

    if data.get('password') is None:
        return EmptyPasswordException()

    if data.get('username') is None:
        raise EmptyEmailException()

    with Session(engine) as _session:
        user_repo = UserRepository(_session)
        user_service = UserService(user_repo)
        user = user_service.get_one(user_id)

    return jsonify({"msg": "All good"}), 201
