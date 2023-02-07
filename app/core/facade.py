from dataclasses import dataclass


@dataclass
class BitcoinWalletCore:
    @classmethod
    def create(cls) -> "BitcoinWalletCore":
        return cls()
