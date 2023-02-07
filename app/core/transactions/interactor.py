from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Transaction:
    from_address: str
    to_address: str
    amount: float
    fee: float

    def get_from_address(self) -> str:
        return self.from_address

    def get_to_address(self) -> str:
        return self.to_address

    def get_amount(self) -> float:
        return self.amount

    def get_fee(self) -> float:
        return self.fee

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        return (
                self.get_from_address() == other.get_from_address()
                and self.get_to_address() == other.get_to_address()
                and self.get_amount() == other.get_amount()
                and self.get_fee() == other.get_fee()
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "fee": self.fee,
        }
