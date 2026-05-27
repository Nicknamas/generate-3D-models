from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from tree_ai.core.db.base_models import Base


class OrganizationModel(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
