import pytest

from app.core.transactions.interactor import Transaction


@pytest.fixture
def transaction() -> Transaction:
    return Transaction(from_address="1", to_address="2", amount=10.3, fee=3)


def test_transaction_get_from_address(transaction: Transaction) -> None:
    assert transaction.get_from_address() == "1"


def test_transaction_get_from_address_neg(transaction: Transaction) -> None:
    assert not transaction.get_from_address() == "13"


def test_transaction_get_to_address(transaction: Transaction) -> None:
    assert transaction.get_to_address() == "2"


def test_transaction_get_to_address_neg(transaction: Transaction) -> None:
    assert not transaction.get_to_address() == "21"


def test_transaction_get_amount(transaction: Transaction) -> None:
    assert transaction.get_amount() == 10.3


def test_transaction_get_amount_neg(transaction: Transaction) -> None:
    assert not transaction.get_amount() == 10.4


def test_transaction_get_fee(transaction: Transaction) -> None:
    assert transaction.get_fee() == 3


def test_transaction_get_fee_neg(transaction: Transaction) -> None:
    assert not transaction.get_fee() == 7


def test_transactions_equals(transaction: Transaction) -> None:
    assert transaction == Transaction(
        from_address="1", to_address="2", amount=10.3, fee=3
    )


def test_transactions_equals_neg_from_address(transaction: Transaction) -> None:
    assert not transaction == Transaction(
        from_address="7", to_address="2", amount=10.3, fee=3
    )


def test_transactions_equals_neg_to_address(transaction: Transaction) -> None:
    assert not transaction == Transaction(
        from_address="1", to_address="23", amount=10.3, fee=3
    )


def test_transactions_equals_neg_amount(transaction: Transaction) -> None:
    assert not transaction == Transaction(
        from_address="1", to_address="2", amount=10.4, fee=3
    )


def test_transactions_equals_neg_fee(transaction: Transaction) -> None:
    assert not transaction == Transaction(
        from_address="1", to_address="2", amount=10.3, fee=7.2
    )
