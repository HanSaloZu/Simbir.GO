from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ALGORITHM, JWT_SECRET_KEY
from database import get_async_session
from models.account import Account
from schemas.token import TokenPayload
from services.account import get_account_by_id
from services.token import get_token_by_value

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/Account/SignIn", scheme_name="JWT"
)


async def get_current_account(
    token: str = Depends(reuseable_oauth),
    session: AsyncSession = Depends(get_async_session),
) -> Account:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        db_token = await get_token_by_value(token, session)
        if db_token is None:
            raise jwt.JWTError
        token_data = TokenPayload(**payload)
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    account = await get_account_by_id(token_data.sub, session)

    if account is None:
        raise HTTPException(
            status_code=403,
            detail="Could not find user",
        )

    return account
