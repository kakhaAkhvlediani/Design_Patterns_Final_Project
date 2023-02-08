import pytest

from app.core.wallets.interactor import Wallet


@pytest.fixture
def wallet() -> Wallet:
    return Wallet(_user_id=10, _address="wallet_address_1", _balance_btc=0)


def test_deposit_balance(wallet: Wallet) -> None:
    amount_to_deposit: float = 100

    wallet.deposit(amount_to_deposit)
    assert wallet.get_balance_in_btc() == amount_to_deposit


def test_deposit_and_withdraw_balance(wallet: Wallet) -> None:
    amount_to_deposit: float = 100
    wallet.deposit(amount_to_deposit)
    assert amount_to_deposit == wallet.get_balance_in_btc()

    amount_to_withdraw: float = amount_to_deposit / 7

    wallet.withdraw(amount_to_withdraw)

    assert wallet.get_balance_in_btc() == (amount_to_deposit - amount_to_withdraw)