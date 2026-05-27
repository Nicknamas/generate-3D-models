from sqlalchemy.sql._typing import _ColumnExpressionArgument
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

    def get_one_or_none(
        self,
        *filters: _ColumnExpressionArgument[bool]
    ):
        stmt = select(OrganizationModel).where(*filters)
        return self.session.scalars(stmt).one_or_none()
