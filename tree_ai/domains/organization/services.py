from dataclasses import asdict
from tree_ai.domains.organization.models import OrganizationModel
from tree_ai.domains.organization.repository import OrganizationRepository
from tree_ai.domains.organization.schemas import OrganizationCreate, OrganizationGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class OrganizationService:
    def __init__(
            self,
            user_repository: OrganizationRepository,
    ):
        self.organization_repository = user_repository

    def create(self, dto: OrganizationCreate) -> OrganizationGet:
        data = asdict(dto)
        model = OrganizationModel(**data)
        self.organization_repository.create(model)
        return OrganizationGet.from_model(model)

    def get_list(self) -> list[OrganizationGet]:
        organization_models = self.organization_repository.get_list()
        return [
            OrganizationGet.from_model(organization_model) for organization_model in organization_models
        ]

    def get_one_or_none(
        self,
        *filters: _ColumnExpressionArgument[bool]
    )-> OrganizationGet:
        user = self.organization_repository.get_one_or_none(id)
        return OrganizationGet.from_model(user)

