from collections import defaultdict
from typing import DefaultDict, Optional, List

from app.core.transactions.interactor import Transaction
from app.core.users.interactor import User


class InMemoryAPIKeyRepository:
    _api_keys_user_ids: DefaultDict[str, int]

    def __init__(self) -> None:
        self._api_keys_user_ids = defaultdict()


    # API_KEY
    def add_api_key_id_pair(self, api_key: str, user_id: int) -> None:
        self._api_keys_user_ids[api_key] = user_id

    def get_user_id_by_api_key(self, api_key: str) -> int:
        return self._api_keys_user_ids.get(api_key, -1)
