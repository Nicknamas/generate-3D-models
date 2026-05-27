from dataclasses import asdict
from typing import Optional
from tree_ai.domains.objects.models import ObjectsModel
from tree_ai.domains.objects.repository import ObjectsRepository
from tree_ai.domains.objects.schemas import ObjectsCreate, ObjectsGet
from sqlalchemy.sql._typing import _ColumnExpressionArgument

class ObjectsService:
    def __init__(self, objects_repository: ObjectsRepository):
        self.objects_repository = objects_repository

    def create(self, dto: ObjectsCreate) -> ObjectsGet:
        data = asdict(dto)
        model = ObjectsModel(**data)
        self.objects_repository.create(model)
        return ObjectsGet.from_model(model)

    def get_list(self) -> list[ObjectsGet]:
        objects_models = self.objects_repository.get_list()
        return [ObjectsGet.from_model(model) for model in objects_models]

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[ObjectsGet]:
        model = self.objects_repository.get_one_or_none(*filters)
        return ObjectsGet.from_model(model) if model else None

    def delete_by_id(self, object_id: int) -> bool:
        """Удалить объект по ID"""
        return self.objects_repository.delete_by_id(object_id)