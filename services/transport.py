from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.transport import Transport


async def get_transport_by_id(id: int, session: AsyncSession):
    query = select(Transport).where(Transport.id == id)
    result = await session.execute(query)
    transport = result.one_or_none()
    return None if transport is None else transport[0]
