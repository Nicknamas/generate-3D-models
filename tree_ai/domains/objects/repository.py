from sqlalchemy import select
from tree_ai.domains.objects.models import ObjectsModel


class ObjectsRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: ObjectsModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self):
        stmt = select(ObjectsModel)
        return self.session.scalars(stmt)

    def get_one(self, id: int):
        stmt = select(ObjectsModel).filter(ObjectsModel.id == id)
        return self.session.scalar(stmt)

    def get_one_or_none(self, *filters):
        stmt = select(ObjectsModel).filter(*filters)
        return self.session.scalar(stmt)

    def delete(self, model: ObjectsModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: int) -> bool:
        model = self.get_one_or_none(ObjectsModel.id == model_id)
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
