from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.transport import Transport


async def get_transport_by_id(id: int, session: AsyncSession):
    query = select(Transport).where(Transport.id == id)
    result = await session.execute(query)
    transport = result.one_or_none()
    return None if transport is None else transport[0]


async def create_transport(
    data,
    session: AsyncSession,
) -> Transport:
    transport = Transport(**data)
    session.add(transport)
    await session.commit()
    return transport


async def update_transport(
    data,
    transport: Transport,
    session: AsyncSession,
):
    transport.can_be_rented = data["can_be_rented"]
    transport.model = data["model"]
    transport.color = data["color"]
    transport.identifier = data["identifier"]
    transport.description = data["description"]
    transport.latitude = data["latitude"]
    transport.longitude = data["longitude"]
    transport.minute_price = data["minute_price"]
    transport.day_price = data["day_price"]
    await session.commit()
    return transport


async def delete_transport_by_id(id: int, session: AsyncSession):
    stmt = delete(Transport).where(Transport.id == id)
    await session.execute(stmt)
    await session.commit()
