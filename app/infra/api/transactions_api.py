# `POST /transactions`
#   - Requires API key
#   - Makes a transaction from one wallet to another
#   - Transaction is free if the same user is the owner of both wallets
#   - System takes a 1.5% (of the transferred amount)
#   fee for transfers to the foreign wallets

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, TransactionResponse
from app.infra.api.dependables import get_core

transactions_api: APIRouter = APIRouter()


@transactions_api.post("/transactions")
def make_transaction(
    api_key: str,
    from_address: str,
    to_address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> TransactionResponse:
    response: TransactionResponse = core.make_transaction(
        api_key=api_key,
        from_address=from_address,
        to_address=to_address,
        amount=amount,
    )
    if response.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response
