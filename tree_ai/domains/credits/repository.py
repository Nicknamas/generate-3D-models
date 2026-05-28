from sqlalchemy import select
from sqlalchemy.sql._typing import _ColumnExpressionArgument
from tree_ai.domains.credits.models import CreditsModel


class CreditsRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: CreditsModel):
        self.session.add(model)
        self.session.commit()
        return model

    def get_list(self):
        stmt = select(CreditsModel)
        return self.session.scalars(stmt).all()

    def get_one(self, id: int):
        stmt = select(CreditsModel).filter(CreditsModel.id == id)
        return self.session.scalar(stmt)

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]):
        stmt = select(CreditsModel).filter(*filters)
        return self.session.scalar(stmt)

    def get_by_user(self, user_id: int):
        stmt = select(CreditsModel).filter(CreditsModel.user_id == user_id)
        return self.session.scalar(stmt)

    def update(self, model: CreditsModel):
        self.session.commit()
        return model

    def delete(self, model: CreditsModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: int) -> bool:
        model = self.get_one_or_none(CreditsModel.id == model_id)
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False

    def delete_by_user(self, user_id: int) -> bool:
        model = self.get_by_user(user_id)
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False