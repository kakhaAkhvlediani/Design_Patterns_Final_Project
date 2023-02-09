# `GET /statistics`
#   - Requires pre-set (hard coded) Admin API key
#   - Returns the total number of transactions and platform profit
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, StatisticsResponse
from app.infra.api.dependables import get_core

statistics_api: APIRouter = APIRouter()


@statistics_api.get("/statistics")
def get_statistics(
    admin_api_key: str, core: BitcoinWalletCore = Depends(get_core)
) -> StatisticsResponse:
    response: StatisticsResponse = core.get_statistics(admin_api_key=admin_api_key)
    if response.status != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response
