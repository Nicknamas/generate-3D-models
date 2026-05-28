from dataclasses import asdict
from typing import Optional
from tree_ai.domains.messages.models import MessagesModel
from tree_ai.domains.messages.repository import MessagesRepository
from tree_ai.domains.messages.schemas import MessagesCreate, MessagesGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class MessagesService:
    def __init__(self, messages_repository: MessagesRepository):
        self.messages_repository = messages_repository

    def create(self, dto: MessagesCreate) -> MessagesGet:
        data = asdict(dto)
        model = MessagesModel(**data)
        self.messages_repository.create(model)
        return MessagesGet.from_model(model)

    def get_list(self, session_id: str | None) -> list[MessagesGet]:
        messages_models = self.messages_repository.get_list(session_id)
        return [MessagesGet.from_model(model) for model in messages_models]

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[MessagesGet]:
        model = self.messages_repository.get_one_or_none(*filters)
        return MessagesGet.from_model(model) if model else None

    def delete_by_id(self, message_id: int) -> None:
        return self.messages_repository.delete_by_id(message_id)
