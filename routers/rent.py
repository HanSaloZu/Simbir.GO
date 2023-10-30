from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from schemas.transport import ExtendedTransportType, TransportBaseCreate
from services.transport import get_transports_available_for_rent

router = APIRouter()


@router.get(
    "/Transport",
    response_model=list[TransportBaseCreate],
    description="Получение транспорта доступного для аренды по параметрам",
)
async def get_transports_for_rent(
    lat: float = 50,
    long: float = 50,
    radius: float = 10,
    type: ExtendedTransportType = ExtendedTransportType.all,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_transports_available_for_rent(
        lat,
        long,
        radius,
        type,
        session,
    )
