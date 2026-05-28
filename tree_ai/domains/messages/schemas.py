from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.messages.models import MessagesModel


@dataclass
class MessagesCreate:
    description: str
    session_id: str
    data: str | None


@dataclass
class MessagesGet:
    id: int
    description: str
    data: str | None
    session_id: str
    user_id: str

    @classmethod
    def from_model(cls, model: MessagesModel) -> Self:
        user_dict = model_as_dict(model)
        return cls(**user_dict)


@dataclass
class MessagesUpdate:
    description: str | None = None

    def update_model(self, model: MessagesModel) -> MessagesModel:
        if self.description:
            model.description = self.description

        return model

