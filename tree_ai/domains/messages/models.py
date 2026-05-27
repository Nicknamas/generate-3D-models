from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from tree_ai.core.db.base_models import Base

class MessageModel(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id', ondelete="CASCADE"))
