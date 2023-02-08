import pytest

from app.core.facade import BitcoinWalletCore, UserResponse, WalletResponse
from app.core.users.interactor import User
from app.infra.in_memory.in_memory_api_key_repository import InMemoryAPIKeyRepository
from app.infra.in_memory.in_memory_transactions_repository import (
    InMemoryTransactionsRepository,
)
from app.infra.in_memory.in_memory_users_repository import InMemoryUsersRepository
from app.infra.in_memory.in_memory_wallets_repository import InMemoryWalletsRepository
from app.infra.utils.hasher import DefaultHashFunction
from app.infra.utils.rate_provider import DefaultRateProvider

rate_provider: DefaultRateProvider = DefaultRateProvider()


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
        rate_provider=DefaultRateProvider(),
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

    assert (
        wallet_response.wallet_info["balance_in_btc"]
        == 1 + 1000 / rate_provider.get_exchange_rate()
    )


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

    expected: float = 1 + (1000 / rate_provider.get_exchange_rate())
    assert wallet_response.wallet_info["balance_in_btc"] == expected

    core.withdraw(
        api_key=user_response.api_key,
        address=wallet_response.wallet_info["address"],
        amount_in_usd=2500,
    )

    wallet_response = core.get_wallet(
        user_response.api_key, wallet_response.wallet_info["address"]
    )
    expected = expected - (2500 / rate_provider.get_exchange_rate())
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

    expected: float = 1 + (1000 / rate_provider.get_exchange_rate())
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
