from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class DefaultCurrencyConverter:
    _exchange_rate: float = 20000.11

    def _get_exchange_rate(self) -> float:
        return self._exchange_rate

    def convert_to_usd(self, amount_in_btc: float) -> float:
        return amount_in_btc * self._get_exchange_rate()

    def convert_to_btc(self, amount_in_usd: float) -> float:
        return amount_in_usd / self._get_exchange_rate()


@dataclass
class CoindeskCurrencyConverter:
    source: str = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"

    def _get_exchange_rate(self) -> float:
        result: Any = requests.get(self.source).json()["bpi"]["USD"]["rate_float"]
        if isinstance(result, float):
            return result
        else:
            return 1

    def convert_to_usd(self, amount_in_btc: float) -> float:
        return amount_in_btc * self._get_exchange_rate()

    def convert_to_btc(self, amount_in_usd: float) -> float:
        return amount_in_usd / self._get_exchange_rate()
