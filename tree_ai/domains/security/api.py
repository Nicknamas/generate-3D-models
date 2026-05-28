from sqlalchemy.orm import Session
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)

from tree_ai.core.db.session import engine
from tree_ai.core.exceptions import EmptyEmailException, EmptyPasswordException, IncorrectEmailOrUsernameException
from tree_ai.domains.security.password import password_hash
from tree_ai.domains.users.models import UserModel
from tree_ai.domains.users.repository import UserRepository


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

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    response = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 201
