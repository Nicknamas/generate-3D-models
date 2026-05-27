from dataclasses import asdict
from typing import Optional
from tree_ai.core.exceptions import UserNotFound
from tree_ai.domains.security.password import password_hash
from tree_ai.domains.users.models import UserModel
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.schemas import UserCreate, UserGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, dto: UserCreate) -> UserGet:
        data = asdict(dto)
        data['password_hash'] = password_hash.hash(data.pop('password'))
        model = UserModel(**data)
        self.user_repository.create(model)
        return UserGet.from_model(model)

    def get_list(self) -> list[UserGet]:
        user_models = self.user_repository.get_list()
        return [UserGet.from_model(model) for model in user_models]

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[UserGet]:
        user = self.user_repository.get_one_or_none(*filters)
        return UserGet.from_model(user) if user else None

    def delete_by_id(self, user_id: int) -> bool:
        """Удалить пользователя по ID"""
        return self.user_repository.delete_by_id(user_id)