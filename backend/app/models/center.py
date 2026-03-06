from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.models.base import Base, TimestampMixin


class Center(Base, TimestampMixin):
    __tablename__ = 'centers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default='UTC')
