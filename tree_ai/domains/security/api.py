from dataclasses import asdict
from tree_ai.core.db.base_models import model_as_dict
from sqlalchemy.orm import Session
from flask import Blueprint, request

from tree_ai.core.db.session import engine
from tree_ai.core.exceptions import EmptyEmailException, EmptyPasswordException, IncorrectEmailOrUsernameException
from tree_ai.domains.security.password import password_hash
from tree_ai.domains.users.models import UserModel
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.schemas import UserGet


router = Blueprint("security", __name__)

@router.post('/login')
def login():
    data: dict[str, str] = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if username is None:
        raise EmptyEmailException()

    if password is None:
        return EmptyPasswordException()

    with Session(engine) as _session:
        user_repo = UserRepository(_session)
        user = user_repo.get_one_or_none(UserModel.username == username.lower())

    if user is None or not password_hash.verify(password, user.password_hash):
        raise IncorrectEmailOrUsernameException()

    user_dto = UserGet.from_model(user)

    return asdict(user_dto), 201
