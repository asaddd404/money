from app.core.security import hash_password, verify_password


def test_password_hash_verify():
    h = hash_password('secret123')
    assert verify_password('secret123', h)
