from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountBase
from schemas.token import TokenBase
from services.account import get_account_by_username, verify_password
from services.token import create_token
from utils.auth import get_current_account

router = APIRouter()


@router.get(
    "/Me",
    response_model=AccountBase,
    description="Получение данных о текущем аккаунте",
)
async def get_authenticated_user(
    account: Account = Depends(get_current_account),
):
    return account


@router.post(
    "/SignIn",
    response_model=TokenBase,
    description="Получение нового jwt токена пользователя",
)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session),
):
    account = await get_account_by_username(username, session)
    if account:
        if verify_password(password, account.hashed_password):
            token = await create_token(account, session)
            return {"access_token": token.value}

    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": "Invalid username or password"}),
    )
