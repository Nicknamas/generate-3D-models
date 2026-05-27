from dataclasses import asdict
from typing import Optional
from tree_ai.domains.organization.models import OrganizationModel
from tree_ai.domains.organization.repository import OrganizationRepository
from tree_ai.domains.organization.schemas import OrganizationCreate, OrganizationGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    def create(self, dto: OrganizationCreate) -> OrganizationGet:
        data = asdict(dto)
        model = OrganizationModel(**data)
        self.organization_repository.create(model)
        return OrganizationGet.from_model(model)

    def get_list(self) -> list[OrganizationGet]:
        organization_models = self.organization_repository.get_list()
        return [OrganizationGet.from_model(model) for model in organization_models]

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[OrganizationGet]:
        model = self.organization_repository.get_one_or_none(*filters)
        return OrganizationGet.from_model(model) if model else None

    def delete_by_id(self, organization_id: int) -> bool:
        """Удалить организацию по ID"""
        return self.organization_repository.delete_by_id(organization_id)