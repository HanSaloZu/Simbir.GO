from passlib.context import CryptContext
from sqlalchemy import delete, select
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


async def create_account(
    data,
    session: AsyncSession,
) -> Account:
    data["hashed_password"] = get_password_hash(data.pop("password"))
    account = Account(**data)
    session.add(account)
    await session.commit()
    return account


async def update_account(
    data,
    account: Account,
    session: AsyncSession,
):
    account.username = data["username"]
    account.hashed_password = get_password_hash(data["password"])
    account.is_admin = data["is_admin"]
    account.balance = data["balance"]
    await session.commit()
    return account


async def delete_account_by_id(id: int, session: AsyncSession):
    stmt = delete(Account).where(Account.id == id)
    await session.execute(stmt)
    await session.commit()
