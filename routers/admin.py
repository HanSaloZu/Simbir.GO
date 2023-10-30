from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.account import Account
from schemas.account import AccountAdminCreateUpdate, AccountBase
from schemas.transport import (ExtendedTransportType,
                               TransportAdminCreateUpdate, TransportBaseCreate)
from services.account import (create_account, delete_account_by_id,
                              get_account_by_id, get_account_by_username,
                              get_accounts_list, update_account)
from services.transport import (create_transport, delete_transport_by_id,
                                get_transport_by_id, get_transports_list,
                                update_transport)
from utils.auth import get_current_admin_account
from utils.exception import (transport_not_found_exception,
                             user_not_found_exception)
from utils.response import nonunique_username_response

account_router = APIRouter()
transport_router = APIRouter()


@account_router.get(
    "/",
    response_model=list[AccountBase],
    description="Получение списка всех аккаунтов",
)
async def list_accounts(
    start: int = 0,
    count: int = 10,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_accounts_list(start, count, session)


@account_router.get(
    "/{id}",
    response_model=AccountBase,
    description="Получение информации об аккаунте по id",
)
async def get_account_info(
    id: int,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    selected_account = await get_account_by_id(id, session)
    if selected_account:
        return selected_account
    raise user_not_found_exception


@account_router.post(
    "/",
    response_model=AccountBase,
    description="Создание администратором нового аккаунта",
)
async def create_account_by_admin(
    data: AccountAdminCreateUpdate,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    new_account = await get_account_by_username(data.username, session)
    if new_account:
        return nonunique_username_response
    return await create_account({**data.model_dump()}, session)


@account_router.put(
    "/{id}",
    response_model=AccountBase,
    description="Изменение администратором аккаунта по id",
)
async def update_account_by_admin(
    id: int,
    data: AccountAdminCreateUpdate,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    selected_account = await get_account_by_id(id, session)
    if selected_account:
        existing_account = await get_account_by_username(data.username, session)
        if existing_account and selected_account.id != existing_account.id:
            return nonunique_username_response
        return await update_account(
            {**data.model_dump()},
            selected_account,
            session,
        )
    raise user_not_found_exception


@account_router.delete(
    "/{id}",
    status_code=204,
    description="Удаление аккаунта по id",
)
async def delete_account(
    id: int,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    selected_account = await get_account_by_id(id, session)
    if selected_account:
        await delete_account_by_id(id, session)
    else:
        raise user_not_found_exception


@transport_router.get(
    "/",
    response_model=list[TransportBaseCreate],
    description="Получение списка всех транспортных средств",
)
async def list_transports(
    start: int = 0,
    count: int = 10,
    transportType: ExtendedTransportType = ExtendedTransportType.all,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_transports_list(start, count, transportType, session)


@transport_router.get(
    "/{id}",
    response_model=TransportBaseCreate,
    description="Получение информации о транспортном средстве по id",
)
async def get_transport_info(
    id: int,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        return transport
    raise transport_not_found_exception


@transport_router.post(
    "/",
    response_model=TransportBaseCreate,
    description="Создание нового транспортного средства",
)
async def create_transport_by_admin(
    data: TransportAdminCreateUpdate,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_transport({**data.model_dump()}, session)


@transport_router.put(
    "/{id}",
    response_model=TransportBaseCreate,
    description="Изменение транспортного средства по id",
)
async def update_transport_by_admin(
    id: int,
    data: TransportAdminCreateUpdate,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        return await update_transport(
            {**data.model_dump()},
            transport,
            session,
        )
    raise transport_not_found_exception


@transport_router.delete(
    "/{id}",
    status_code=204,
    description="Удаление транспорта по id",
)
async def delete_transport(
    id: int,
    account: Account = Depends(get_current_admin_account),
    session: AsyncSession = Depends(get_async_session),
):
    transport = await get_transport_by_id(id, session)
    if transport:
        await delete_transport_by_id(id, session)
    else:
        raise transport_not_found_exception
