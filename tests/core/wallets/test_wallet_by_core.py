import pytest
from starlette import status

from app.core.facade import BitcoinWalletCore
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

rate_provider: DefaultCurrencyConverter = DefaultCurrencyConverter()


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


def test_create_more_than_three_wallets(user: User, core: BitcoinWalletCore) -> None:
    api_key: str = core.register_user(
        username=user.get_username(), password=user.get_password()
    ).api_key
    core.create_wallet(api_key=api_key)
    core.create_wallet(api_key=api_key)
    core.create_wallet(api_key=api_key)
    assert core.create_wallet(api_key=api_key).status == status.HTTP_400_BAD_REQUEST


def test_create_wallet_with_wrong_api_key(user: User, core: BitcoinWalletCore) -> None:
    api_key: str = core.register_user(
        username=user.get_username(), password=user.get_password()
    ).api_key

    assert core.create_wallet(api_key=api_key + "1").status == status.HTTP_403_FORBIDDEN


def test_get_wallet_with_wrong_api_key(user: User, core: BitcoinWalletCore) -> None:
    api_key: str = core.register_user(
        username=user.get_username(), password=user.get_password()
    ).api_key
    address: str = core.create_wallet(api_key=api_key).wallet_info["address"]
    assert (
        core.get_wallet(api_key=api_key + "1", address=address).status
        == status.HTTP_403_FORBIDDEN
    )


def test_get_wallet_with_wrong_wallet_address(
    user: User, core: BitcoinWalletCore
) -> None:
    api_key: str = core.register_user(
        username=user.get_username(), password=user.get_password()
    ).api_key
    address: str = core.create_wallet(api_key=api_key).wallet_info["address"]
    assert (
        core.get_wallet(api_key=api_key, address=address + "w").status
        == status.HTTP_404_NOT_FOUND
    )


def test_get_wallet_with_api_key_of_other_user(
    user: User, core: BitcoinWalletCore
) -> None:
    api_key: str = core.register_user(
        username=user.get_username(), password=user.get_password()
    ).api_key
    address: str = core.create_wallet(api_key=api_key).wallet_info["address"]
    api_key = core.register_user(
        username=user.get_username() + "a", password=user.get_password()
    ).api_key
    assert (
        core.get_wallet(api_key=api_key, address=address).status
        == status.HTTP_403_FORBIDDEN
    )
