from flask_jwt_extended import jwt_required
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.domains.organization.models import OrganizationModel
from tree_ai.domains.organization.repository import OrganizationRepository
from tree_ai.domains.organization.schemas import OrganizationCreate
from tree_ai.domains.organization.services import OrganizationService


router = Blueprint("organizations", __name__)


@router.post('/organizations')
def create_organization():
    data: dict[str, Any] = request.get_json()
    organization_dto = OrganizationCreate(**data)

    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)
        organization_get_dto = organization_service.create(organization_dto)

    return asdict(organization_get_dto)


@router.get('/organizations')
@jwt_required()
def get_users():
    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)
        list_organization_get_dto = organization_service.get_list()

    return [asdict(organization_get_dto) for organization_get_dto in list_organization_get_dto]


@router.get('/organizations/<int:organization_id>')
def get_user(organization_id: int):
    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)
        organization = organization_service.get_one_or_none(OrganizationModel.id == organization_id)

    return asdict(organization)
