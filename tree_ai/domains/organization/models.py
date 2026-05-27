from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tree_ai.core.db.base_models import Base
from tree_ai.domains.users.models import UserModel


class OrganizationModel(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    users: Mapped[list[UserModel]] = relationship()