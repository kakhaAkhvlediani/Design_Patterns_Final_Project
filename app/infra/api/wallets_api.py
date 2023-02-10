# `POST /wallets`
#   - Requires API key
#   - Create BTC wallet
#   - Deposits 1 BTC (or 100000000 satoshis) automatically to the new wallet
#   - User may register up to 3 wallets
#   - Returns wallet address and balance in BTC and USD
from typing import Any, Dict

# `GET /wallets/{address}`
#   - Requires API key
#   - Returns wallet address and balance in BTC and USD
#
#
# `GET /wallets/{address}/transactions`
#   - Requires API key
#   - returns transactions related to the wallet
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, WalletResponse
from app.infra.api.dependables import get_core

wallets_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    200: {"status_code": status.HTTP_200_OK, "msg": "Wallet Returned"},
    201: {"status_code": status.HTTP_201_CREATED, "msg": "Wallet Created"},
    400: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "msg": "You can create maximum 3 wallets",
    },
    403: {
        "status_code": status.HTTP_403_FORBIDDEN,
        "msg": "Wrong api_key for this wallet",
    },
    404: {"status_code": status.HTTP_404_NOT_FOUND, "msg": "Wallet Not Found"},
}


@wallets_api.post("/wallets", status_code=status.HTTP_201_CREATED)
def create_wallet(
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.create_wallet(api_key=api_key)
    if status_translator[response.status]["status_code"] != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response


@wallets_api.get("/wallets/{address}", status_code=status.HTTP_200_OK)
def get_wallet(
    address: str,
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.get_wallet(api_key=api_key, address=address)
    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response


@wallets_api.get("/wallets/{address}/transactions", status_code=status.HTTP_200_OK)
def get_transactions_for_this_wallet(
    address: str,
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.get_transactions_of_wallet(
        api_key=api_key, address=address
    )
    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response
