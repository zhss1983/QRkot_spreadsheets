from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas import CharityProjectDB
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    response_model=List[CharityProjectDB],
    response_model_exclude=['fully_invested']
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    reports = await charity_project_crud.get_projects_by_completion_rate(
        session)
    rows = len(reports)
    spreadsheetid = await spreadsheets_create(wrapper_services, rows)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, reports, wrapper_services)
    return reports
