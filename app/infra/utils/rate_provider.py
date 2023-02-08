from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class DefaultRateProvider:
    _exchange_rate: float = 20000.11

    def get_exchange_rate(self) -> float:
        return self._exchange_rate


@dataclass
class ExchangeRateProvider:
    source: str = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"

    def get_exchange_rate(self) -> float:
        result: Any = requests.get(self.source).json()["bpi"]["USD"]["rate_float"]
        if isinstance(result, float):
            return result
        else:
            return 1
