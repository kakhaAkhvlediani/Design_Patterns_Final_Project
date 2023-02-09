from typing import Optional

import pytest

from app.core.facade import BitcoinWalletCore, UserResponse
from app.core.users.interactor import User
from app.infra.in_memory.in_memory_api_key_repository import InMemoryAPIKeyRepository
from app.infra.in_memory.in_memory_transactions_repository import (
    InMemoryTransactionsRepository,
)
from app.infra.in_memory.in_memory_users_repository import InMemoryUsersRepository
from app.infra.in_memory.in_memory_wallets_repository import InMemoryWalletsRepository
from app.infra.utils.fee_strategy import FeeRateStrategy
from app.infra.utils.hasher import DefaultHashFunction
from app.infra.utils.rate_provider import DefaultCurrencyConverter


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
    )


@pytest.fixture
def user() -> User:
    username: str = "Lean"
    password: str = "password"

    return User(_user_id=0, _username=username, _password=password)


@pytest.fixture
def hasher() -> DefaultHashFunction:
    hasher: DefaultHashFunction = DefaultHashFunction()
    return hasher


def test_if_user_gets_saved(core: BitcoinWalletCore, user: User) -> None:
    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
    assert core.get_user_id_by_api_key(api_key=response.api_key) != -1


def test_if_user_gets_saved_again(core: BitcoinWalletCore, user: User) -> None:
    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
    assert core.get_user_id_by_api_key(api_key=response.api_key) != -1

    response = core.register_user(user.get_username(), user.get_password())
    assert core.get_user_id_by_api_key(api_key=response.api_key) == -1


def test_valid_api_key_response(core: BitcoinWalletCore, user: User) -> None:
    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
    assert core.get_user_id_by_api_key(api_key=response.api_key) != -1


def test_invalid_api_key_response(core: BitcoinWalletCore, user: User) -> None:
    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
    assert core.get_user_id_by_api_key(api_key=response.api_key + "12") == -1


def test_get_user(core: BitcoinWalletCore, user: User) -> None:
    core.register_user(user.get_username(), user.get_password())
    user_from_database: Optional[User] = core.get_user(user.get_username())

    assert user_from_database is not None


def test_get_user_neg_wrong_username(core: BitcoinWalletCore, user: User) -> None:
    core.register_user(user.get_username(), user.get_password())
    user_from_database: Optional[User] = core.get_user(user.get_password())

    assert user_from_database is None


def test_api_key_prefix(core: BitcoinWalletCore, user: User) -> None:
    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
    api_key: str = response.api_key
    assert api_key.startswith("api_key_")


def test_password_gets_hashed(core: BitcoinWalletCore, user: User) -> None:
    core.register_user(user.get_username(), user.get_password())
    user_from_database: Optional[User] = core.get_user(user.get_username())
    assert user_from_database is not None
    assert user.get_password() != user_from_database.get_password()


def test_password_gets_hashed_correctly(
        core: BitcoinWalletCore, user: User, hasher: DefaultHashFunction
) -> None:
    core.register_user(user.get_username(), user.get_password())
    user_from_database: Optional[User] = core.get_user(user.get_username())

    assert user_from_database is not None
    hashed_password = hasher(user.get_password())

    assert user_from_database.get_password() == hashed_password


def test_register_user_changes(core: BitcoinWalletCore, user: User) -> None:
    core.register_user(username=user.get_username(), password=user.get_password())

    get_user1: User = core.get_user(username=user.get_username())

    assert user != get_user1
    assert user.get_user_id() == get_user1.get_user_id()
    assert user.get_username() == get_user1.get_username()
    assert user.get_password() != get_user1
