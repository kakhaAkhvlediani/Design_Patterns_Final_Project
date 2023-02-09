# `GET /statistics`
#   - Requires pre-set (hard coded) Admin API key
#   - Returns the total number of transactions and platform profit
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, StatisticsResponse
from app.infra.api.dependables import get_core

statistics_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    200: {"status_code": status.HTTP_200_OK, "msg": "Statistic Returned"},
    403: {"status_code": status.HTTP_403_FORBIDDEN, "msg": "Wrong api_key for this wallet"},
}


@statistics_api.get("/statistics", status_code=status.HTTP_200_OK)
def get_statistics(
        admin_api_key: str, core: BitcoinWalletCore = Depends(get_core)
) -> StatisticsResponse:
    response: StatisticsResponse = core.get_statistics(admin_api_key=admin_api_key)
    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"]
        )
    return response
