from datetime import datetime, timezone

from jose import jwt
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
