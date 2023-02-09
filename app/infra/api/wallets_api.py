# `POST /wallets`
#   - Requires API key
#   - Create BTC wallet
#   - Deposits 1 BTC (or 100000000 satoshis) automatically to the new wallet
#   - User may register up to 3 wallets
#   - Returns wallet address and balance in BTC and USD

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


@wallets_api.post("/wallets", status_code=status.HTTP_201_CREATED)
def create_wallet(
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.create_wallet(api_key=api_key)
    if response.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response


@wallets_api.get("/wallets/{address}", status_code=status.HTTP_200_OK)
def get_wallet(
    address: str,
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.get_wallet(api_key=api_key, address=address)
    if response.status != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response


@wallets_api.get("/wallets/{address}/transactions")
def get_transactions_for_this_wallet(
    address: str,
    api_key: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.get_transactions_of_wallet(
        api_key=api_key, address=address
    )
    if response.status != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response


@wallets_api.post("/wallets/{address}/deposit")
def deposit(
    api_key: str,
    address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.deposit(
        api_key=api_key,
        address=address,
        amount_in_usd=amount,
    )
    if response.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response


@wallets_api.post("/wallets/{address}/withdraw")
def withdraw(
    api_key: str,
    address: str,
    amount: float,
    core: BitcoinWalletCore = Depends(get_core),
) -> WalletResponse:
    response: WalletResponse = core.withdraw(
        api_key=api_key,
        address=address,
        amount_in_usd=amount,
    )
    if response.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response
