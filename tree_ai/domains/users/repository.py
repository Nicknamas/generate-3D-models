from sqlalchemy import select
from tree_ai.domains.users.models import UserModel


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: UserModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self):
        stmt = select(UserModel)
        return self.session.scalars(stmt)

    def get_one(self, id: int):
        stmt = select(UserModel).filter(UserModel.id == id)
        return self.session.scalar(stmt)
