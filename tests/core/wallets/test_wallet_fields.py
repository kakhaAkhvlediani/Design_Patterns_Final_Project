import pytest

from app.core.wallets.interactor import Wallet


@pytest.fixture
def wallet() -> Wallet:
    return Wallet(
        _user_id=10,
        _address="wallet_address_1",
        _balance_btc=10.7,
    )


def test_owner(wallet: Wallet) -> None:
    assert wallet.get_owner_id() == 10


def test_address(wallet: Wallet) -> None:
    assert wallet.get_address() == "wallet_address_1"


def test_balance(wallet: Wallet) -> None:
    assert wallet.get_balance_in_btc() == 10.7


def test_equals_method(wallet: Wallet) -> None:
    assert wallet == Wallet(
        _user_id=10,
        _address="wallet_address_1",
        _balance_btc=10.7,
    )


def test_equals_method_neg(wallet: Wallet) -> None:
    assert wallet != wallet.to_dict()
