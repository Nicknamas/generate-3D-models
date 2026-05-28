from sqlalchemy import select
from tree_ai.domains.sessions.models import SessionModel


class SessionRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: SessionModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self):
        stmt = select(SessionModel)
        return self.session.scalars(stmt)

    def get_one(self, id: int):
        stmt = select(SessionModel).filter(SessionModel.id == id)
        return self.session.scalar(stmt)

    def get_one_or_none(self, *filters):
        stmt = select(SessionModel).filter(*filters)
        return self.session.scalar(stmt)

    def delete(self, model: SessionModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: int) -> bool:
        model = self.get_one_or_none(SessionModel.id == model_id)
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
