from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: int
    iat: int
