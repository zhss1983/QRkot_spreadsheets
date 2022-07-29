from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.invest import invested_amount
from app.api.validator import (
    charity_project_permission_to_delete,
    check_charity_project_name_duplicate,
    check_charity_project_update_blocked,
    check_data_for_update_in_json,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter()


@router.get(
    "/", response_model=List[CharityProjectDB], response_model_exclude_none=True
)
async def get_charity_project(session: AsyncSession = Depends(get_async_session)):
    """Получает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    dependencies=(Depends(current_superuser),),
    response_model_exclude_none=True,
    response_model=CharityProjectDB,
)
async def post_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Создает благотворительный проект."""
    await check_charity_project_name_duplicate(
        session, project_name=charity_project.name
    )
    db_obj = charity_project_crud.get_object_from_dict(charity_project)
    await charity_project_crud.create(db_obj, session)
    await invested_amount(session)
    return await charity_project_crud.refresh(db_obj, session)


@router.delete(
    "/{project_id}",
    dependencies=(Depends(current_superuser),),
    response_model_exclude_none=True,
    response_model=CharityProjectDB,
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть."""
    db_obj = await charity_project_permission_to_delete(session, project_id=project_id)
    return await charity_project_crud.remove(db_obj, session)


@router.patch(
    "/{project_id}",
    dependencies=(Depends(current_superuser),),
    response_model_exclude_none=True,
    response_model=CharityProjectDB,
)
async def get_charity_project_by_id(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Только для суперюзеров.

    Закрытый проект нельзя редактировать, также нельзя установить требуемую
    сумму меньше уже вложенной."""
    check_data_for_update_in_json(charity_project)
    db_obj = await check_charity_project_update_blocked(
        session, project_id=project_id, full_amount=charity_project.full_amount
    )
    await check_charity_project_name_duplicate(
        session, project_name=charity_project.name, project_id=project_id
    )
    await charity_project_crud.update(db_obj, charity_project, session)
    await invested_amount(session)
    return await charity_project_crud.refresh(db_obj, session)
