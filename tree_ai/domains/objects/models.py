from datetime import timezone
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from tree_ai.core.db.base_models import Base

class ObjectsModel(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column(String(500), nullable=False)
    message_id: Mapped[int] = mapped_column(ForeignKey('messages.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
