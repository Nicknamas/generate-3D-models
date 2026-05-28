from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from tree_ai.core.db.base_models import Base


class CreditsModel(Base):
    __tablename__ = 'credits'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False, unique=True)
    amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
