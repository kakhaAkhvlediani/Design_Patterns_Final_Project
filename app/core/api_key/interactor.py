from dataclasses import dataclass
from typing import Protocol


@dataclass
class APIKeyIDPair:
    user_id: int
    api_key: str


class IAPIKeysRepository(Protocol):
    def add_api_key_id_pair(self, api_key: str, user_id: int) -> None:
        pass

    def get_user_id_by_api_key(self, api_key: str) -> int:
        pass


@dataclass
class APIKeyInteractor:
    _api_key_repository: IAPIKeysRepository

    def add_api_key_id_pair(self, api_key: str, user_id: int) -> None:
        return self._api_key_repository.add_api_key_id_pair(
            api_key=api_key, user_id=user_id
        )

    def get_user_id_by_api_key(self, api_key: str) -> int:
        return self._api_key_repository.get_user_id_by_api_key(api_key=api_key)
