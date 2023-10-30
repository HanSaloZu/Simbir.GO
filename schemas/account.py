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


class AccountCreateUpdate(BaseModel):
    username: str = Field(min_length=1, max_length=250)
    password: str = Field(min_length=1, max_length=250)


class AccountAdminCreateUpdate(AccountCreateUpdate):
    is_admin: bool = Field(alias="isAdmin")
    balance: float

    class Config:
        from_attributes = True
        populate_by_name = True
