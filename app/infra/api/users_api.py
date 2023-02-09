# `POST /users`
#   - Registers user
#   - Returns API key that can authenticate all subsequent requests for this user
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, UserResponse
from app.infra.api.dependables import get_core

users_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    201: {"status_code": status.HTTP_201_CREATED, "msg": "User Created"},
    400: {"status_code": status.HTTP_400_BAD_REQUEST, "msg": "User is Registered"},
}


@users_api.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(
    username: str, password: str, core: BitcoinWalletCore = Depends(get_core)
) -> UserResponse:
    response: UserResponse = core.register_user(username=username, password=password)
    if status_translator[response.status]["status_code"] != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response
