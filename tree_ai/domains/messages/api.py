from flask_jwt_extended import jwt_required
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.domains.messages.models import MessagesModel
from tree_ai.domains.messages.repository import MessagesRepository
from tree_ai.domains.messages.schemas import MessagesCreate
from tree_ai.domains.messages.services import MessagesService


router = Blueprint("messages", __name__)


@router.post('/messages')
def create_messages():
    data: dict[str, Any] = request.get_json()
    messages_dto = MessagesCreate(**data)

    with Session(engine) as session:
        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)
        messages_get_dto = messages_service.create(messages_dto)

    return asdict(messages_get_dto)


@router.get('/messages')
@jwt_required()
def get_messages():
    with Session(engine) as session:
        messages_repo = MessagesRepository(session)
        messages_service = MessagesService(messages_repo)
        list_messages_get_dto = messages_service.get_list()

    return [asdict(message) for message in list_messages_get_dto]


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