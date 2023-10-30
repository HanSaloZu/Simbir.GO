from sqlalchemy.ext.asyncio import AsyncSession

from models.account import Account


async def hesoyam(account: Account, session: AsyncSession):
    account.balance += 250000
    await session.commit()
    return account
