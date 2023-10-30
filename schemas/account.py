from pydantic import BaseModel, Field


class AccountBalance(BaseModel):
    id: int
    username: str
    balance: float
