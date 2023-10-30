from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountBalance
from services.account import get_account_by_id
from services.payment import hesoyam
from utils.auth import get_current_account
from utils.exception import user_not_found_exception

router = APIRouter()


@router.post("/Hesoyam/{accountId}", response_model=AccountBalance)
async def pay(
    accountId: int,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    selected_account = await get_account_by_id(accountId, session)
    if selected_account:
        if account.is_admin:
            return await hesoyam(selected_account, session)
        elif selected_account.id == account.id:
            return await hesoyam(account, session)
        else:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise user_not_found_exception
