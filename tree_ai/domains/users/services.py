import bcrypt
from dataclasses import asdict
from tree_ai.core.db.base_models import model_as_dict
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

    def get_one(self, id) -> UserGet:
        user = self.user_repository.get_one(id)
        return UserGet.from_model(user)

