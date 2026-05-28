import datetime
from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.messages.models import MessagesModel
from tree_ai.domains.objects.schemas import ObjectsGet


@dataclass
class MessagesCreate:
    request: str
    session_id: str
    script: str | None
    description: str | None


@dataclass
class MessagesGet:
    id: int
    request: str
    description: str | None
    script: str | None
    session_id: str
    user_id: str
    created_at: datetime.datetime
    object: ObjectsGet | None = None

    @classmethod
    def from_model(cls, model: MessagesModel) -> Self:
        user_dict = model_as_dict(model)
        if getattr(model, "object", None) is not None:
            user_dict["object"] = ObjectsGet.from_model(model.object)
        return cls(**user_dict)


@dataclass
class MessagesUpdate:
    description: str | None = None

    def update_model(self, model: MessagesModel) -> MessagesModel:
        if self.description:
            model.description = self.description

        return model

