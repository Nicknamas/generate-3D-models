from typing import Self
from dataclasses import dataclass

from tree_ai.core.db.base_models import model_as_dict
from tree_ai.domains.security.password import password_hash
from tree_ai.domains.users.models import UserModel


@dataclass
class UserCreate:
    username: str
    password: str


@dataclass
class UserGet:
    id: int
    username: str

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        user_dict = model_as_dict(model)
        user_dict.pop('password_hash')
        return cls(**user_dict)


@dataclass
class UserUpdate:
    username: str | None = None
    password: str | None = None

    def update_model(self, model: UserModel) -> UserModel:
        if self.username:
            model.username = self.username

        if self.password:
            model.password_hash = password_hash.hash(self.password)

        return model

