from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


@dataclass
class User:
    _user_id: int
    _username: str
    _password: str

    def get_user_id(self) -> int:
        return self._user_id

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return (
            self.get_username() == other.get_username()
            and self.get_password() == other.get_password()
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.get_user_id(),
            "username": self.get_username(),
            "password": self.get_password(),  # TODO maybe better to delete
        }


class IUserRepository(Protocol):
    def add_user(self, new_user: User) -> bool:
        pass

    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    def get_all_users(self) -> List[User]:
        pass

    def get_max_user_id(self) -> int:
        pass


@dataclass
class UsersInteractor:
    _users_repository: IUserRepository

    def register_user(self, username: str, password: str) -> Optional[User]:
        new_user_id: int = self._users_repository.get_max_user_id()
        new_user: User = User(
            _user_id=new_user_id, _username=username, _password=password
        )
        is_new_user: bool = self._users_repository.add_user(new_user=new_user)
        return new_user if is_new_user else None

    def get_user(self, username: str) -> Optional[User]:
        return self._users_repository.get_user_by_username(username=username)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self._users_repository.get_user_by_id(user_id)

    def get_all_users(self) -> List[User]:
        return self._users_repository.get_all_users()
