from pydantic import BaseModel, Field


class AccountBalance(BaseModel):
    id: int
    username: str
    balance: float


class AccountBase(AccountBalance):
    is_admin: bool = Field(
        alias="isAdmin",
    )

    class Config:
        from_attributes = True
        populate_by_name = True
