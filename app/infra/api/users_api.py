# `POST /users`
#   - Registers user
#   - Returns API key that can authenticate all subsequent requests for this user

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import BitcoinWalletCore, UserResponse
from app.infra.api.dependables import get_core

users_api: APIRouter = APIRouter()


@users_api.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(
    username: str, password: str, core: BitcoinWalletCore = Depends(get_core)
) -> UserResponse:
    response: UserResponse = core.register_user(username=username, password=password)
    if response.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status, detail=response.msg)
    return response
