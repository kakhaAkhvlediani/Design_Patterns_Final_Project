from dataclasses import dataclass


@dataclass
class Transaction:
    from_address: str
    to_address: str
    amount: float
    fee: float
