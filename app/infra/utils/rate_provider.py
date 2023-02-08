from dataclasses import dataclass


@dataclass
class DefaultRateProvider:
    _exchange_rate: float = 20000.11

    def get_exchange_rate(self) -> float:
        return self._exchange_rate
