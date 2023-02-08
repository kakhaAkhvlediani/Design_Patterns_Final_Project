from typing import Optional

import pytest

from app.core.facade import BitcoinWalletCore, UserResponse
from app.core.users.interactor import User
from app.infra.in_memory.InMemoryAPIKeyRepository import InMemoryAPIKeyRepository
from app.infra.in_memory.InMemoryWalletsRepository import InMemoryWalletsRepository
from app.infra.utils.hasher import DefaultHashFunction
from app.infra.in_memory.InMemoryUsersRepository import InMemoryUsersRepository


@pytest.fixture
def core() -> BitcoinWalletCore:
    users_repository: InMemoryUsersRepository = InMemoryUsersRepository()
    wallets_repository: InMemoryWalletsRepository = InMemoryWalletsRepository()
    api_key_repository: InMemoryAPIKeyRepository = InMemoryAPIKeyRepository()
    return BitcoinWalletCore.create(
        users_repository=users_repository,
        wallets_repository=wallets_repository,
        api_key_repository=api_key_repository,
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

    response: UserResponse = core.register_user(
        user.get_username(), user.get_password()
    )
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