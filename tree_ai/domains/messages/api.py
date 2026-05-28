from tree_ai.core.exceptions import NeedMoreMoney, UserNotFound
from tree_ai.domains.credits.services import CreditsService
from tree_ai.domains.credits.repository import CreditsRepository
from tree_ai.domains.users.models import UserModel
from flask_jwt_extended import get_jwt_identity
import base64

from flask_jwt_extended import jwt_required
from dataclasses import asdict
from tree_ai.core.ai import get_creating_script, get_detailed_prompt_by_ai
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.domains.messages.models import MessagesModel
from tree_ai.domains.messages.repository import MessagesRepository
from tree_ai.domains.messages.schemas import MessagesCreate
from tree_ai.domains.messages.services import MessagesService
from tree_ai.domains.objects.repository import ObjectsRepository
from tree_ai.domains.objects.services import ObjectsService
from tree_ai.domains.users.repository import UserRepository


router = Blueprint("messages", __name__)


@router.post('/messages')
@jwt_required()
def create_messages():
    data: dict[str, Any] = request.get_json()
    prompt = data.get('request')

    if not prompt:
        return {"error": "Missing required field: 'request'"}, 400

    current_username = get_jwt_identity()

    with Session(engine) as session:
        user_repo = UserRepository(session)
        current_user = user_repo.get_one_or_none(UserModel.id == current_username)

        if not current_user:
            raise UserNotFound()

        credits_repo = CreditsRepository(session)
        credits_service = CreditsService(credits_repo)

        cost_per_message = 1
        balance = credits_service.get_balance(current_user.id)

        if balance < cost_per_message:
            raise NeedMoreMoney()

        detailed_prompt = get_detailed_prompt_by_ai(prompt)
        data['description'] = detailed_prompt

        script = get_creating_script(detailed_prompt)
        data['script'] = script
        
        data['user_id'] = current_user.id 

        messages_dto = MessagesCreate(**data)

        spend_result = credits_service.spend_credits(current_user.id, cost_per_message)
        if not spend_result.success:
            return {"error": spend_result.message}, 400

        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)

        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)

        messages_get_dto = messages_service.create(messages_dto)

        objects_service.create(
            title=str(prompt), 
            message_id=messages_get_dto.id
        )

        result = asdict(messages_get_dto)
        result['credits_spent'] = cost_per_message
        result['new_balance'] = spend_result.new_balance

    return result, 201


@router.get('/messages')
@jwt_required()
def get_messages():
    session_id = request.args.get('session_id')

    with Session(engine) as session:
        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)
        list_messages_dto = messages_service.get_list(session_id)

    result = []
    for msg_dto in list_messages_dto:
        msg_dict = asdict(msg_dto)
        
        if msg_dict.get('object') is not None:
            obj_data = msg_dict['object'].get('data')
            if isinstance(obj_data, bytes):
                msg_dict['object']['data'] = base64.b64encode(obj_data).decode('utf-8')
                
        result.append(msg_dict)

    return result, 200


@router.get('/messages/<int:messages_id>')
def get_message(messages_id: int):
    with Session(engine) as session:
        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)
        messages = messages_service.get_one_or_none(MessagesModel.id == messages_id)
        if not messages:
            return {"error": "Message not found"}, 404
    return asdict(messages)


@router.delete('/messages/<int:messages_id>')
@jwt_required()
def delete_message(messages_id: int):
    with Session(engine) as session:
        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)

        if messages_service.delete_by_id(messages_id):
            return {"msg": "Message deleted successfully"}, 200
        else:
            return {"error": "Message not found"}, 404
