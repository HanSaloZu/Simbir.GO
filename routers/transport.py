from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.transport import TransportBaseCreate, TransportUpdate
from services.transport import (create_transport, delete_transport_by_id,
                                get_transport_by_id, update_transport)
from utils.auth import get_current_account
from utils.exception import (access_denied_exception,
                             transport_not_found_exception)

router = APIRouter()


@router.get(
    "/{id}",
    response_model=TransportBaseCreate,
    description="Получение информации о транспорте по id",
)
async def get_transport_info(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        return transport
    raise transport_not_found_exception


@router.post(
    "/",
    response_model=TransportBaseCreate,
    description="Добавление нового транспорта",
)
async def create(
    data: TransportBaseCreate,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_transport(
        {**data.model_dump(), "owner_id": account.id}, session
    )


@router.put(
    "/{id}",
    response_model=TransportBaseCreate,
    description="Изменение транспорта оп id",
)
async def update(
    id: int,
    data: TransportUpdate,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        if transport.owner_id == account.id:
            return await update_transport(
                {**data.model_dump()},
                transport,
                session,
            )
        else:
            raise access_denied_exception
    raise transport_not_found_exception


@router.delete(
    "/{id}",
    status_code=204,
    description="Удаление транспорта по id",
)
async def delete(
    id: int,
    account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        if transport.owner_id == account.id:
            await delete_transport_by_id(id, session)
        else:
            raise access_denied_exception
    else:
        raise transport_not_found_exception
