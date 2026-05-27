from sqlalchemy.sql._typing import _ColumnExpressionArgument
import bcrypt
from dataclasses import asdict
from tree_ai.core.exceptions import UserNotFound
from tree_ai.domains.users.models import UserModel
from tree_ai.domains.users.repository import UserRepository
from tree_ai.domains.users.schemas import UserCreate, UserGet


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def create(self, dto: UserCreate) -> UserGet:
        data = asdict(dto)
        salt = bcrypt.gensalt()
        data['password_hash'] = bcrypt.hashpw(
            data.pop('password').encode("utf-8"), salt
        )
        model = UserModel(**data)
        self.user_repository.create(model)
        return UserGet.from_model(model)
    
    def get_list(self) -> list[UserGet]:
        user_models = self.user_repository.get_list()
        return [
            UserGet.from_model(user_model) for user_model in user_models
        ]

    def get_one_or_none(
        self, 
        *filters: _ColumnExpressionArgument[bool]
    ) -> UserGet:
        user = self.user_repository.get_one_or_none(*filters)
        if user is None:
            raise UserNotFound()

        return UserGet.from_model(user)

