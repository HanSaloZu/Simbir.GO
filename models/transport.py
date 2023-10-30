from sqlalchemy import Boolean, Column, Double, ForeignKey, Integer, String

from database import Base
from models.account import Account


class Transport(Base):
    __tablename__ = "transports"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
    )
    can_be_rented = Column(Boolean, nullable=False)
    transport_type = Column(String, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    identifier = Column(String, nullable=False)
    description = Column(String, nullable=True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    minute_price = Column(Double, nullable=True)
    day_price = Column(Double, nullable=True)
    owner_id = Column(
        Integer, ForeignKey(Account.id, ondelete="CASCADE"), nullable=False
    )
