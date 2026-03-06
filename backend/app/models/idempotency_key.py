from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, String, JSON, UniqueConstraint
from app.models.base import Base, TimestampMixin


class IdempotencyKey(Base, TimestampMixin):
    __tablename__ = 'idempotency_keys'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    method: Mapped[str] = mapped_column(String(16), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    response_body: Mapped[dict] = mapped_column(JSON, nullable=False)

    __table_args__ = (UniqueConstraint('key', 'user_id', 'endpoint', 'method', name='uq_idempotency_key_scope'),)
