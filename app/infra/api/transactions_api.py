# `POST /transactions`
#   - Requires API key
#   - Makes a transaction from one wallet to another
#   - Transaction is free if the same user is the owner of both wallets
#   - System takes a 1.5% (of the transferred amount)
#   fee for transfers to the foreign wallets

from fastapi import APIRouter, Depends
from starlette import status

from app.core.facade import BitcoinWalletCore
from app.infra.api.dependables import get_core

transactions_api: APIRouter = APIRouter()


@transactions_api.post("/transactions", status_code=status.HTTP_201_CREATED)
def make_transaction(
    api_key: str,
    from_address: str,
    to_address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> str:
    return "response"
