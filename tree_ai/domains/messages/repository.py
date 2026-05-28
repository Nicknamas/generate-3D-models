from sqlalchemy import select
from tree_ai.domains.messages.models import MessagesModel


class MessagesRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: MessagesModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self, session_id: str | None):
        if session_id is not None:
            stmt = select(MessagesModel).where(MessagesModel.session_id == int(session_id))
            return self.session.scalars(stmt)

        stmt = select(MessagesModel)
        return self.session.scalars(stmt)

    def get_one(self, id: int):
        stmt = select(MessagesModel).filter(MessagesModel.id == id)
        return self.session.scalar(stmt)

    def get_one_or_none(self, *filters):
        stmt = select(MessagesModel).filter(*filters)
        return self.session.scalar(stmt)

    def delete(self, model: MessagesModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: int) -> None:
        model = self.get_one(model_id)
        self.delete(model)
