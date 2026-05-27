from dataclasses import asdict
from tree_ai.domains.sessions.models import SessionModel
from tree_ai.domains.sessions.repository import SessionRepository
from tree_ai.domains.sessions.schemas import SessionCreate, SessionGet


class SessionService:
    def __init__(
        self,
        user_repository: SessionRepository,
    ):
        self.session_repository = user_repository

    def create(self, dto: SessionCreate) -> SessionGet:
        data = asdict(dto)
        model = SessionModel(**data)
        self.session_repository.create(model)
        return SessionGet.from_model(model)
    
    def get_list(self) -> list[SessionGet]:
        session_models = self.session_repository.get_list()
        return [
            SessionGet.from_model(session_model) for session_model in session_models
        ]

    def get_one(self, id) -> SessionGet:
        user = self.session_repository.get_one(id)
        return SessionGet.from_model(user)

