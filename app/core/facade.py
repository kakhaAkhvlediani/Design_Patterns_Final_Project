from asyncio import Protocol
from dataclasses import dataclass
from typing import Optional

from starlette import status

from app.core.api_key.interactor import APIKeyInteractor, IAPIKeyRepository
from app.core.users.interactor import UsersInteractor, IUserRepository, User
from app.infra.utils.hasher import DefaultHashFunction


@dataclass
class UserResponse:
    status: int
    msg: str = ""
    api_key: str = ""


class IHasher(Protocol):
    def use_my_hash(self, *args: object) -> str:
        pass

    def __call__(self, *args: object) -> str:
        return self.use_my_hash(args)


@dataclass
class BitcoinWalletCore:
    _users_interactor: UsersInteractor
    _api_key_interactor: APIKeyInteractor
    _hash: IHasher

    @classmethod
    def create(
            cls,
            users_repository: IUserRepository,
            api_key_interactor_repository: IAPIKeyRepository,
            hash_function: IHasher = DefaultHashFunction(),
    ) -> "BitcoinWalletCore":
        return cls(
            _users_interactor=UsersInteractor(_users_repository=users_repository),
            _api_key_interactor=APIKeyInteractor(_api_key_repository=api_key_interactor_repository),
            _hash=hash_function,
        )

    # USER RESPONSE
    def _generate_api_key(self, args: object) -> str:
        return "api_key_" + self._hash(args)

    def get_user_id_by_api_key(self, api_key: str) -> int:
        return self._api_key_interactor.get_user_id_by_api_key(api_key)

    def get_user(self, username: str) -> Optional[User]:
        return self._users_interactor.get_user(username)

    def is_correct_api_key(self, api_key: str) -> bool:
        return self.get_user_id_by_api_key(api_key=api_key) != -1

    def register_user(self, username: str, password: str) -> UserResponse:
        api_key: str = self._generate_api_key((username, password))
        user: Optional[User] = self._users_interactor.register_user(
            username=username, password=self._hash(password)
        )
        if user is None:
            return UserResponse(status=status.HTTP_400_BAD_REQUEST, msg="Is Registered")

        self._api_key_interactor.add_api_key_id_pair(
            api_key=api_key, user_id=user.get_user_id()
        )

        return UserResponse(
            status=status.HTTP_201_CREATED, msg="Registered", api_key=api_key
        )
