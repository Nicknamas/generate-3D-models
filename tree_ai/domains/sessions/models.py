from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tree_ai.core.db.base_models import Base
from tree_ai.domains.messages.models import MessageModel

class SessionModel(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False, default='Новая сессия')
    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="session", 
        cascade="all, delete-orphan"
    )
