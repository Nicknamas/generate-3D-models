from sqlalchemy.orm import relationship
from datetime import timezone
from datetime import datetime
from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column
from tree_ai.core.db.base_models import Base

class ObjectsModel(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    message_id: Mapped[int] = mapped_column(
        ForeignKey('messages.id', ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    message: Mapped["MessagesModel"] = relationship(back_populates="object")
