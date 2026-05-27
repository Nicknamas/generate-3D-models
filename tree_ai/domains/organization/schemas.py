from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.organization.models import OrganizationModel


@dataclass
class OrganizationCreate:
    title: str


@dataclass
class OrganizationGet:
    id: int
    title: str

    @classmethod
    def from_model(cls, model: OrganizationModel) -> Self:
        user_dict = model_as_dict(model)
        return cls(**user_dict)


@dataclass
class OrganizationUpdate:
    title: str | None = None

    def update_model(self, model: OrganizationModel) -> OrganizationModel:
        if self.title:
            model.title = self.title

        return model

