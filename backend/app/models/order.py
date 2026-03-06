import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Enum, String, Index
from app.models.base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    created = 'created'
    approved = 'approved'
    handed_over = 'handed_over'
    completed = 'completed'
    cancelled = 'cancelled'
    rejected = 'rejected'


class Order(Base, TimestampMixin):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey('centers.id'), index=True, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.created)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)


class OrderItem(Base):
    __tablename__ = 'order_items'
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_snapshot: Mapped[int] = mapped_column(Integer, nullable=False)
    product_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)

Index('ix_orders_center_status', Order.center_id, Order.status)
