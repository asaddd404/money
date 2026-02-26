from app.models.order import OrderStatus


def test_order_status_created():
    assert OrderStatus.created.value == 'created'
