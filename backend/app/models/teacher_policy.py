from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from app.models.base import Base, TimestampMixin


class TeacherPolicy(Base, TimestampMixin):
    __tablename__ = 'teacher_policies'
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    max_points_per_award: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
