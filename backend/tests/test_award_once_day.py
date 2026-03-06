from app.models.transaction import TransactionType


def test_award_enum_present():
    assert TransactionType.award.value == 'award'
