import enum
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Enum, String, Date, DateTime, Index
from app.models.base import Base, TimestampMixin


class TransactionType(str, enum.Enum):
    award = 'award'
    hold = 'hold'
    release = 'release'
    purchase = 'purchase'


class Transaction(Base, TimestampMixin):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    group_id: Mapped[int | None] = mapped_column(ForeignKey('groups.id'), nullable=True)
    order_id: Mapped[int | None] = mapped_column(ForeignKey('orders.id'), nullable=True)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    awarded_by: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    award_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    awarded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    available_after: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    held_after: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

Index('ix_transactions_center_student', Transaction.center_id, Transaction.student_id)
