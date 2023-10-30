from sqlalchemy import Boolean, Column, Double, Integer, String

from database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
    )
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    balance = Column(Double, nullable=False, default=0)
    is_admin = Column(Boolean, nullable=False, default=False)
