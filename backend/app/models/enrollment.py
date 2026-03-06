import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Enum, Index
from app.models.base import Base, TimestampMixin


class EnrollmentStatus(str, enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'


class Enrollment(Base, TimestampMixin):
    __tablename__ = 'enrollments'
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    status: Mapped[EnrollmentStatus] = mapped_column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.pending)

Index('ix_enrollments_center_status', Enrollment.center_id, Enrollment.status)
