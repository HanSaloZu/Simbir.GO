from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.account import Account

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


async def get_account_by_username(username: str, session: AsyncSession):
    query = select(Account).where(Account.username == username)
    result = await session.execute(query)
    account = result.one_or_none()
    return None if account is None else account[0]
