from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountBase
from services.account import get_account_by_id, get_accounts_list
from utils.auth import get_current_admin_account
from utils.exception import user_not_found_exception

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
