from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.invest import invested_amount
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import UserTable
from app.schemas import DonationCreate, DonationDB, DonationShow

router = APIRouter()


@router.get(
    '/',
    dependencies=(Depends(current_superuser),),
    response_model=list[DonationDB]
)
async def get_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Получает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model_exclude_none=True,
    response_model=list[DonationShow],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: UserTable = Depends(current_user),
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_attribute(
        'user_id', user.id, session)
    return donations.all()


@router.post(
    '/',
    response_model=DonationShow,
    response_model_exclude_none=True,
)
async def get_charity_project(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: UserTable = Depends(current_user)
):
    """Сделать пожертвование."""
    db_obj = donation_crud.get_object_from_dict(donation, user)
    await donation_crud.create(db_obj, session)
    await invested_amount(session)
    return await donation_crud.refresh(db_obj, session)
