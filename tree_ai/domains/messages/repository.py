from sqlalchemy import select

from tree_ai.domains.messages.models import MessageModel


class MessageRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: MessageModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self):
        stmt = select(MessageModel)
        return self.session.scalars(stmt)

    def get_one(self, id: int):
        stmt = select(MessageModel).filter(MessageModel.id == id)
        return self.session.scalar(stmt)
