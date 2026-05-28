from datetime import timezone
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tree_ai.core.db.base_models import Base
from tree_ai.domains.messages.models import MessagesModel

class SessionModel(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False, default='Новая сессия')
    messages: Mapped[list[MessagesModel]] = relationship(
        cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
