from sqlalchemy import Column, ForeignKey, Integer, String

from database import Base
from models.account import Account


class Token(Base):
    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
    )
    value = Column(String, nullable=False, index=True)
    account_id = Column(
        Integer, ForeignKey(Account.id, ondelete="CASCADE"), nullable=False
    )
