import base64
from typing import Any
from dataclasses import asdict
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session

from tree_ai.core.db.session import engine
from tree_ai.domains.objects.models import ObjectsModel
from tree_ai.domains.objects.repository import ObjectsRepository
from tree_ai.domains.objects.services import ObjectsService

router = Blueprint("objects", __name__)


@router.post('/objects')
@jwt_required()
def create_objects():
    data: dict[str, Any] = request.get_json()
    
    title = data.get('title')
    message_id = data.get('message_id')

    if not title or not message_id:
        return {"error": "Missing required fields: 'title' and 'message_id'"}, 400

    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        
        objects_get_dto = objects_service.create(
            title=title,
            message_id=int(message_id)
        )
        
    return asdict(objects_get_dto), 201


@router.get('/objects')
@jwt_required()
def get_objects():
    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        list_objects_get_dto = objects_service.get_list()

    result = []
    for obj in list_objects_get_dto:
        obj_dict = asdict(obj)
        if isinstance(obj_dict.get('data'), bytes):
            obj_dict['data'] = base64.b64encode(obj_dict['data']).decode('utf-8')
        result.append(obj_dict)

    return result, 200


@router.get('/objects/<int:objects_id>')
@jwt_required()
def get_object(objects_id: int):
    with Session(engine) as session:
        objects_repo = ObjectsRepository(session)
        objects_service = ObjectsService(objects_repo)
        obj = objects_service.get_one_or_none(ObjectsModel.id == objects_id)
        
        if not obj:
            return {"error": "Object not found"}, 404
            
    obj_dict = asdict(obj)
    if isinstance(obj_dict.get('data'), bytes):
        obj_dict['data'] = base64.b64encode(obj_dict['data']).decode('utf-8')
        
    return obj_dict, 200


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
