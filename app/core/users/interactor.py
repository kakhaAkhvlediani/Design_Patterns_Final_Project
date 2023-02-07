from dataclasses import dataclass
from typing import Any, Dict


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
