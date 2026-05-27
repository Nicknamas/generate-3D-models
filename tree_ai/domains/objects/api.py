from flask_jwt_extended import jwt_required
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.domains.objects.models import ObjectsModel
from tree_ai.domains.objects.repository import ObjectsRepository
from tree_ai.domains.objects.schemas import ObjectsCreate
from tree_ai.domains.objects.services import ObjectsService


router = Blueprint("objects", __name__)


@router.post('/objects')
def create_objects():
    data: dict[str, Any] = request.get_json()
    objects_dto = ObjectsCreate(**data)

    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        objects_get_dto = objects_service.create(objects_dto)

    return asdict(objects_get_dto)


@router.get('/objects')
@jwt_required()
def get_objects():
    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        list_objects_get_dto = objects_service.get_list()

    return [asdict(obj) for obj in list_objects_get_dto]


@router.get('/objects/<int:objects_id>')
def get_object(objects_id: int):
    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        obj = objects_service.get_one_or_none(ObjectsModel.id == objects_id)
        if not obj:
            return {"error": "Object not found"}, 404
    return asdict(obj)


@router.delete('/objects/<int:objects_id>')
@jwt_required()
def delete_object(objects_id: int):
    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)

        if objects_service.delete_by_id(objects_id):
            return {"msg": "Object deleted successfully"}, 200
        else:
            return {"error": "Object not found"}, 404