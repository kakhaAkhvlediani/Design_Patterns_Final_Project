# `GET /statistics`
#   - Requires pre-set (hard coded) Admin API key
#   - Returns the total number of transactions and platform profit
from fastapi import APIRouter, Depends
from starlette import status

from app.core.facade import BitcoinWalletCore
from app.infra.api.dependables import get_core

statistics_api: APIRouter = APIRouter()


@statistics_api.get("/statistics", status_code=status.HTTP_200_OK)
def get_statistics(
    admin_api_key: str, core: BitcoinWalletCore = Depends(get_core)
) -> str:
    return "response"
