from app.models.order import OrderStatus


def test_order_status_cancelled():
    assert OrderStatus.cancelled.value == 'cancelled'
