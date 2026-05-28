from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from dataclasses import asdict
from tree_ai.core.db.session import engine
from sqlalchemy.orm import Session

from tree_ai.domains.sessions.models import SessionModel
from tree_ai.domains.sessions.repository import SessionRepository
from tree_ai.domains.sessions.schemas import SessionCreate
from tree_ai.domains.sessions.services import SessionService


router = Blueprint("sessions", __name__)


@router.post('/sessions')
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    session_dto = SessionCreate(user_id)

    with Session(engine) as session:
        session_repo = SessionRepository(session)
        session_service = SessionService(session_repo)
        session_get_dto = session_service.create(session_dto)

    return asdict(session_get_dto)


@router.get('/sessions')
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()

    with Session(engine) as _session:
        session_repo = SessionRepository(_session)
        session_service = SessionService(session_repo)
        list_session_get_dto = session_service.get_list(user_id)

    return [asdict(sess) for sess in list_session_get_dto]


@router.get('/sessions/<int:session_id>')
@jwt_required()
def get_session(session_id: int):
    with Session(engine) as _session:
        session_repo = SessionRepository(_session)
        session_service = SessionService(session_repo)
        session = session_service.get_one_or_none(SessionModel.id == session_id)
        if not session:
            return {"error": "Session not found"}, 404
    return asdict(session)


@router.delete('/sessions/<int:session_id>')
@jwt_required()
def delete_session(session_id: int):
    with Session(engine) as _session:
        session_repo = SessionRepository(_session)
        session_service = SessionService(session_repo)

        if session_service.delete_by_id(session_id):
            return {"msg": "Session deleted successfully"}, 200
        else:
            return {"error": "Session not found"}, 404
