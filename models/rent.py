from datetime import datetime

from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String

from database import Base
from models.account import Account
from models.transport import Transport


class Rent(Base):
    __tablename__ = "rents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
    )
    time_start = Column(DateTime, nullable=False, default=datetime.now())
    time_end = Column(DateTime, nullable=True)
    type = Column(String, nullable=False)
    price_of_unit = Column(Double, nullable=True)
    final_price = Column(Double, nullable=True)
    transport_id = Column(
        Integer, ForeignKey(Transport.id, ondelete="CASCADE"), nullable=False
    )
    renter_id = Column(
        Integer, ForeignKey(Account.id, ondelete="CASCADE"), nullable=False
    )
