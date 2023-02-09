# `POST /transactions`
#   - Requires API key
#   - Makes a transaction from one wallet to another
#   - Transaction is free if the same user is the owner of both wallets
#   - System takes a 1.5% (of the transferred amount)
#   fee for transfers to the foreign wallets
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, TransactionResponse
from app.infra.api.dependables import get_core

transactions_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    201: {"status_code": status.HTTP_201_CREATED, "msg": "Transaction Created"},
    400: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "msg": "Not enough funds in the wallet",
    },
    403: {
        "status_code": status.HTTP_403_FORBIDDEN,
        "msg": "Wrong api_key for this wallet",
    },
    404: {"status_code": status.HTTP_404_NOT_FOUND, "msg": "Wallet Not Found"},
}


@transactions_api.post("/transactions", status_code=status.HTTP_201_CREATED)
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
    if status_translator[response.status]["status_code"] != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response


@transactions_api.post(
    "/wallets/{address}/deposit", status_code=status.HTTP_201_CREATED
)
def deposit(
    api_key: str,
    address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> TransactionResponse:
    response: TransactionResponse = core.deposit(
        api_key=api_key,
        address=address,
        amount_in_usd=amount,
    )
    if status_translator[response.status]["status_code"] != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response


@transactions_api.post(
    "/wallets/{address}/withdraw", status_code=status.HTTP_201_CREATED
)
def withdraw(
    api_key: str,
    address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> TransactionResponse:
    response: TransactionResponse = core.withdraw(
        api_key=api_key,
        address=address,
        amount_in_usd=amount,
    )
    if status_translator[response.status]["status_code"] != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response
