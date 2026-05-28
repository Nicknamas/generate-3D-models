import datetime
from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.sessions.models import SessionModel


@dataclass
class SessionCreate:
    user_id: int
    title: str | None = None


@dataclass
class SessionGet:
    id: int
    title: str
    created_at: datetime.datetime
    user_id: int | None

    @classmethod
    def from_model(cls, model: SessionModel) -> Self:
        user_dict = model_as_dict(model)
        return cls(**user_dict)


@dataclass
class SessionUpdate:
    title: str | None = None

    def update_model(self, model: SessionModel) -> SessionModel:
        if self.title:
            model.title = self.title

        return model

