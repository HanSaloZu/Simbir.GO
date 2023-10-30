from datetime import datetime, timezone

from jose import jwt
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ALGORITHM, JWT_SECRET_KEY
from models.account import Account
from models.token import Token


async def create_token(account: Account, session: AsyncSession) -> Token:
    to_encode = {
        "sub": str(account.id),
        "iat": datetime.now(tz=timezone.utc),
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    token = Token(account_id=account.id, value=encoded_jwt)
    session.add(token)
    await session.commit()
    return token


async def delete_token_by_value(value: str, session: AsyncSession):
    stmt = delete(Token).where(Token.value == value)
    await session.execute(stmt)
    await session.commit()


async def get_token_by_value(value: str, session: AsyncSession):
    query = select(Token).where(Token.value == value)
    result = await session.execute(query)
    token = result.one_or_none()
    return None if token is None else token[0]
