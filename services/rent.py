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
