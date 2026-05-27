from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from tree_ai.core.db.base_models import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

