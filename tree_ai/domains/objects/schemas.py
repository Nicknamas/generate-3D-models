from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.objects.models import ObjectsModel


@dataclass
class ObjectsCreate:
    title: str


@dataclass
class ObjectsGet:
    id: int
    title: str

    @classmethod
    def from_model(cls, model: ObjectsModel) -> Self:
        user_dict = model_as_dict(model)
        return cls(**user_dict)


@dataclass
class ObjectsUpdate:
    title: str | None = None

    def update_model(self, model: ObjectsModel) -> ObjectsModel:
        if self.title:
            model.title = self.title

        return model

