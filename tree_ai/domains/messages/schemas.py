from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.messages.models import MessagesModel


@dataclass
class MessagesCreate:
    title: str


@dataclass
class MessagesGet:
    id: int
    title: str

    @classmethod
    def from_model(cls, model: MessagesModel) -> Self:
        user_dict = model_as_dict(model)
        return cls(**user_dict)


@dataclass
class MessagesUpdate:
    title: str | None = None

    def update_model(self, model: MessagesModel) -> MessagesModel:
        if self.title:
            model.title = self.title

        return model

