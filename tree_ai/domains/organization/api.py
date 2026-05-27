from flask_jwt_extended import jwt_required
from dataclasses import asdict
from tree_ai.core.db.session import engine
from typing import Any
from flask import Blueprint, request
from sqlalchemy.orm import Session

from tree_ai.core.exceptions import OrganizationNotFound
from tree_ai.domains.organization.models import OrganizationModel
from tree_ai.domains.organization.repository import OrganizationRepository
from tree_ai.domains.organization.schemas import OrganizationCreate
from tree_ai.domains.organization.services import OrganizationService


router = Blueprint("organizations", __name__)


@router.post('/organizations')
@jwt_required()
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
def get_organizations():
    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)
        list_organization_get_dto = organization_service.get_list()

    return [asdict(org) for org in list_organization_get_dto]


@router.get('/organizations/<int:organization_id>')
@jwt_required()
def get_organization(organization_id: int):
    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)
        organization = organization_service.get_one_or_none(OrganizationModel.id == organization_id)
        if not organization:
            raise OrganizationNotFound()
    return asdict(organization)


@router.delete('/organizations/<int:organization_id>')
@jwt_required()
def delete_organization(organization_id: int):
    with Session(engine) as session:
        organization_repo = OrganizationRepository(session)
        organization_service = OrganizationService(organization_repo)

        if organization_service.delete_by_id(organization_id):
            return {"msg": "Organization deleted successfully"}, 200
        else:
            return {"error": "Organization not found"}, 404