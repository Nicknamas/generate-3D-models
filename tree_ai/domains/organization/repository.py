from sqlalchemy import select
from tree_ai.domains.organization.models import OrganizationModel


class OrganizationRepository:
    def __init__(self, session):
        self.session = session

    def create(self, model: OrganizationModel):
        self.session.add(model)
        self.session.commit()

    def get_list(self):
        stmt = select(OrganizationModel)
        return self.session.scalars(stmt)

    def get_one_or_none(self, *filters):
        stmt = select(OrganizationModel).where(*filters)
        return self.session.scalar(stmt)

    def delete(self, model: OrganizationModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: int) -> bool:
        model = self.get_one_or_none(OrganizationModel.id == model_id)
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False