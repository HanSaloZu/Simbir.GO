from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountAdminCreateUpdate, AccountBase
from services.account import (create_account, get_account_by_id,
                              get_account_by_username, get_accounts_list)
from utils.auth import get_current_admin_account
from utils.exception import user_not_found_exception
from utils.response import nonunique_username_response

account_router = APIRouter()


@account_router.get(
    "/",
    response_model=list[AccountBase],
    description="Получение списка всех аккаунтов",
)
async def list_accounts(
    start: int = 0,
    count: int = 10,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_accounts_list(start, count, session)


@account_router.get(
    "/{id}",
    response_model=AccountBase,
    description="Получение информации об аккаунте по id",
)
async def get_account_info(
    id: int,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    selected_account = await get_account_by_id(id, session)
    if selected_account:
        return selected_account
    raise user_not_found_exception


@account_router.post(
    "/",
    response_model=AccountBase,
    description="Создание администратором нового аккаунта",
)
async def create_account_by_admin(
    data: AccountAdminCreateUpdate,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    new_account = await get_account_by_username(data.username, session)
    if new_account:
        return nonunique_username_response
    return await create_account({**data.model_dump()}, session)
