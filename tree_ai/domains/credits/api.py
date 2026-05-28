from flask_jwt_extended import jwt_required, get_jwt_identity
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.core.exceptions import CreditsNotFound, UserNotFound
from tree_ai.domains.credits.repository import CreditsRepository
from tree_ai.domains.credits.schemas import CreditsCreate
from tree_ai.domains.credits.services import CreditsService
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.models import UserModel


router = Blueprint("credits", __name__)


@router.post('/credits')
@jwt_required()
def create_credits():
    data: dict[str, Any] = request.get_json()

    with Session(engine) as session:
        credits_dto = CreditsCreate(**data)
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        credits_get_dto = credits_service.create(credits_dto)

    return asdict(credits_get_dto), 201


@router.post('/credits/add')
@jwt_required()
def add_credits():
    data: dict[str, Any] = request.get_json()
    amount = data.get('amount', 0)
    print(amount)

    current_username = get_jwt_identity()

    with Session(engine) as session:
        user_repo = UserRepository(session)
        current_user = user_repo.get_one_or_none(UserModel.id == current_username)

        if not current_user:
            raise UserNotFound()

        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        result = credits_service.add_credits(current_user.id, amount)

    return asdict(result), 200 if result.success else 400


@router.post('/credits/spend')
@jwt_required()
def spend_credits():
    data: dict[str, Any] = request.get_json()
    amount = data.get('amount', 0)

    current_username = get_jwt_identity()

    with Session(engine) as session:
        user_repo = UserRepository(session)
        current_user = user_repo.get_one_or_none(UserModel.id == current_username)

        if not current_user:
            raise UserNotFound()

        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        result = credits_service.spend_credits(current_user.id, amount)

    return asdict(result), 200 if result.success else 400


@router.get('/credits')
@jwt_required()
def get_all_credits():
    with Session(engine) as session:
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        credits_list = credits_service.get_list()

    return [asdict(c) for c in credits_list]


@router.get('/credits/me')
@jwt_required()
def get_my_credits():
    current_id = get_jwt_identity()

    with Session(engine) as session:
        user_repo = UserRepository(session)
        current_user = user_repo.get_one_or_none(UserModel.id == current_id)

        if not current_user:
            UserNotFound()

        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        credits = credits_service.get_by_user(current_user.id)

        if not credits:
            return {
                "user_id": current_user.id,
                "amount": 0,
                "message": "No credits record found, balance is 0"
            }, 200

    return asdict(credits)


@router.get('/credits/me/balance')
@jwt_required()
def get_my_balance():
    current_username = get_jwt_identity()

    with Session(engine) as session:
        user_repo = UserRepository(session)
        current_user = user_repo.get_one_or_none(UserModel.id == current_username)

        if not current_user:
            raise UserNotFound()

        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        balance = credits_service.get_balance(current_user.id)

    return {"user_id": current_user.id, "balance": balance}


@router.get('/credits/user/<int:user_id>')
@jwt_required()
def get_user_credits(user_id: int):
    with Session(engine) as session:
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        credits = credits_service.get_by_user(user_id)

        if not credits:
            raise CreditsNotFound()

    return asdict(credits)


@router.get('/credits/<int:credits_id>')
@jwt_required()
def get_credits_by_id(credits_id: int):
    with Session(engine) as session:
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)
        credits = credits_service.get_by_id(credits_id)

        if not credits:
            raise CreditsNotFound()

    return asdict(credits)


@router.delete('/credits/<int:credits_id>')
@jwt_required()
def delete_credits(credits_id: int):
    with Session(engine) as session:
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)

        if credits_service.delete_by_id(credits_id):
            return {"msg": "Credits deleted successfully"}, 200
        else:
            raise CreditsNotFound()


@router.delete('/credits/user/<int:user_id>')
@jwt_required()
def delete_credits_by_user(user_id: int):
    with Session(engine) as session:
        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)

        if credits_service.delete_by_user(user_id):
            return {"msg": f"Credits for user {user_id} deleted successfully"}, 200
        else:
            raise CreditsNotFound()
