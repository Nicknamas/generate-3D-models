from dataclasses import asdict
from typing import Optional
from tree_ai.domains.sessions.models import SessionModel
from tree_ai.domains.sessions.repository import SessionRepository
from tree_ai.domains.sessions.schemas import SessionCreate, SessionGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class SessionService:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository

    def create(self, dto: SessionCreate) -> SessionGet:
        data = asdict(dto)
        model = SessionModel(**data)
        self.session_repository.create(model)
        return SessionGet.from_model(model)

    def get_list(self, user_id: str | None) -> list[SessionGet]:
        session_models = self.session_repository.get_list(user_id)
        return [SessionGet.from_model(model) for model in session_models]

    def get_one(self, id: int) -> Optional[SessionGet]:
        model = self.session_repository.get_one(id)
        return SessionGet.from_model(model) if model else None

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[SessionGet]:
        model = self.session_repository.get_one_or_none(*filters)
        return SessionGet.from_model(model) if model else None

    def delete_by_id(self, session_id: int) -> bool:
        """Удалить сессию по ID"""
        return self.session_repository.delete_by_id(session_id)
