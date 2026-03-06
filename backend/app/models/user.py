import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum, ForeignKey, Index
from app.models.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    student = 'student'
    teacher = 'teacher'
    manager = 'manager'
    admin = 'admin'


class User(Base, TimestampMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)

Index('ix_users_center_role', User.center_id, User.role)
