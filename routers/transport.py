from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from schemas.transport import TransportBaseCreate
from services.transport import get_transport_by_id
from utils.exception import transport_not_found_exception

router = APIRouter()


@router.get(
    "/{id}",
    response_model=TransportBaseCreate,
    description=" Получение информации о транспорте по id",
)
async def get_transport_info(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        return transport
    raise transport_not_found_exception
