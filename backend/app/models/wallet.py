from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from app.models.base import Base, TimestampMixin


class Wallet(Base, TimestampMixin):
    __tablename__ = 'wallets'
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    available_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    held_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_spent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
