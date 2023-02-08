from dataclasses import dataclass


@dataclass
class FeeRateStrategy:
    fee_rate_for_different_owners: float = 0.015
    fee_rate_for_same_owner: float = 0
    fee_rate_for_deposit: float = 0
    fee_rate_for_withdraw: float = 0

    def get_fee_rate_for_different_owners(self) -> float:
        return self.fee_rate_for_different_owners

    def get_fee_rate_for_same_owner(self) -> float:
        return self.fee_rate_for_same_owner

    def get_fee_rate_for_deposit(self) -> float:
        return self.fee_rate_for_deposit

    def get_fee_rate_for_withdraw(self) -> float:
        return self.fee_rate_for_withdraw
