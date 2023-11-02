from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.rent import RentBase, RentType
from schemas.transport import ExtendedTransportType, TransportBase
from services.rent import create_rent, get_rent_by_id, is_transport_in_rent
from services.transport import (get_transport_by_id,
                                get_transports_available_for_rent)
from utils.auth import get_current_account
from utils.exception import (access_denied_exception, rent_not_found_exception,
                             transport_not_found_exception)

router = APIRouter()


@router.get(
    "/Transport",
    response_model=list[TransportBase],
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


@router.get(
    "/{id}",
    response_model=RentBase,
    description="Получение информации об аренде по id",
)
async def get_rent_info(
    id: int,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    rent = await get_rent_by_id(id, session)
    if rent:
        transport = await get_transport_by_id(rent.transport_id, session)
        if rent.renter_id == account.id or transport.owner_id == account.id:
            return rent
        else:
            raise access_denied_exception
    raise rent_not_found_exception


@router.post(
    "/New/{transportId}",
    response_model=RentBase,
    description="Аренда транспорта в личное пользование",
)
async def rent_transport(
    transportId: int,
    rentType: RentType,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(transportId, session)
    if transport:
        if transport.owner_id == account.id:
            raise HTTPException(
                status_code=403,
                detail="You already own this transport",
            )
        if transport.can_be_rented and not await is_transport_in_rent(
            transportId,
            session,
        ):
            price_of_unit = transport.day_price
            if rentType == RentType.minutes:
                price_of_unit = transport.minute_price
            return await create_rent(
                {
                    "type": rentType,
                    "price_of_unit": price_of_unit,
                    "transport_id": transportId,
                    "renter_id": account.id,
                },
                session,
            )
        else:
            raise HTTPException(
                status_code=403,
                detail="This transport cannot be rented",
            )
    else:
        raise transport_not_found_exception
