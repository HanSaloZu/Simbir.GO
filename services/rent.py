from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.rent import Rent


async def create_rent(
    data,
    session: AsyncSession,
) -> Rent:
    rent = Rent(**data)
    session.add(rent)
    await session.commit()
    return rent


async def is_transport_in_rent(
    transport_id: int,
    session: AsyncSession,
) -> bool:
    query = select(Rent).where(Rent.time_end == None, Rent.transport_id == transport_id)
    result = await session.execute(query)
    return result.one_or_none() is not None
