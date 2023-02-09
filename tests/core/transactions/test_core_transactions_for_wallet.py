import pytest

from app.core.facade import BitcoinWalletCore, UserResponse, WalletResponse
from app.core.users.interactor import User
from app.infra.in_memory.in_memory_api_key_repository import InMemoryAPIKeyRepository
from app.infra.in_memory.in_memory_transactions_repository import (
    InMemoryTransactionsRepository,
)
from app.infra.in_memory.in_memory_users_repository import InMemoryUsersRepository
from app.infra.in_memory.in_memory_wallets_repository import InMemoryWalletsRepository
from app.infra.utils.currency_converter import DefaultCurrencyConverter
from app.infra.utils.fee_strategy import FeeRateStrategy
from app.infra.utils.generator import DefaultUniqueValueGenerators
from app.infra.utils.hasher import DefaultHashFunction

currency_converter: DefaultCurrencyConverter = DefaultCurrencyConverter()


@pytest.fixture
def core() -> BitcoinWalletCore:
    users_repository: InMemoryUsersRepository = InMemoryUsersRepository()
    wallets_repository: InMemoryWalletsRepository = InMemoryWalletsRepository()
    api_key_repository: InMemoryAPIKeyRepository = InMemoryAPIKeyRepository()
    transactions_repository: InMemoryTransactionsRepository = (
        InMemoryTransactionsRepository()
    )
    return BitcoinWalletCore.create(
        users_repository=users_repository,
        wallets_repository=wallets_repository,
        api_key_repository=api_key_repository,
        transactions_repository=transactions_repository,
        hash_function=DefaultHashFunction(),
        currency_converter=DefaultCurrencyConverter(),
        fee_strategy=FeeRateStrategy(),
        unique_value_generator=DefaultUniqueValueGenerators(),
    )


@pytest.fixture
def user() -> User:
    username: str = "Lean"
    password: str = "password"

    return User(_user_id=0, _username=username, _password=password)


def test_deposit_balance(user: User, core: BitcoinWalletCore) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    core.deposit(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=1000,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    assert wallet_response.wallet_info[
               "balance_in_btc"
           ] == 1 + currency_converter.convert_to_btc(amount_in_usd=1000)


def test_deposit_withdraw(user: User, core: BitcoinWalletCore) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    core.deposit(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=1000,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    expected: float = 1 + currency_converter.convert_to_btc(amount_in_usd=1000)
    assert wallet_response.wallet_info["balance_in_btc"] == expected

    core.withdraw(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=2500,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )
    expected = expected - currency_converter.convert_to_btc(amount_in_usd=2500)
    assert wallet_response.wallet_info["balance_in_btc"] == expected


def test_withdraw_more_than_on_balance(user: User, core: BitcoinWalletCore) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    core.deposit(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=1000,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    expected: float = 1 + currency_converter.convert_to_btc(amount_in_usd=1000)
    assert wallet_response.wallet_info["balance_in_btc"] == expected

    core.withdraw(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=250000,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )
    assert wallet_response.wallet_info["balance_in_btc"] == expected


def test_deposit_neg_wrong_api_key_deposit(user: User, core: BitcoinWalletCore) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    assert (
            core.deposit(
                api_key=user_response.api_key + "2",
                address=wallet_response.wallet_info["address"],
                amount_in_usd=1000,
            ).status
            == 403
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    expected: float = 1
    assert wallet_response.wallet_info["balance_in_btc"] == expected


def test_withdraw_neg_wrong_api_key(
        user: User, core: BitcoinWalletCore
) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    assert (
            core.withdraw(
                api_key=user_response.api_key + "2",
                address=wallet_response.wallet_info["address"],
                amount_in_usd=25,
            ).status
            == 403
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    assert wallet_response.wallet_info["balance_in_btc"] == 1


def test_withdraw_neg_wrong_wallet_address(
        user: User, core: BitcoinWalletCore
) -> None:
    user_response: UserResponse = core.register_user(
        username=user.get_username() + "a", password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    assert (
            core.withdraw(
                api_key=user_response.api_key,
                address=wallet_response.wallet_info["address"] + "2",
                amount_in_usd=25,
            ).status
            == 404
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    assert wallet_response.wallet_info["balance_in_btc"] == 1


def test_withdraw_neg_wrong_owner_key(
        user: User, core: BitcoinWalletCore
) -> None:
    api_key: str = core.register_user(
        username=user.get_username() + "a", password=user.get_password()
    ).api_key
    user_response: UserResponse = core.register_user(
        username=user.get_username(), password=user.get_password()
    )
    wallet_response: WalletResponse = core.create_wallet(api_key=user_response.api_key)

    assert (
            core.withdraw(
                api_key=api_key,
                address=wallet_response.wallet_info["address"],
                amount_in_usd=25,
            ).status
            == 403
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )

    assert wallet_response.wallet_info["balance_in_btc"] == 1
