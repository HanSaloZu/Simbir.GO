from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountBase
from services.account import get_accounts_list
from utils.auth import get_current_admin_account

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
