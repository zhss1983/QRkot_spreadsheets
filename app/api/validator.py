from http import HTTPStatus
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import HTTPException
from app.crud import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
    session: AsyncSession,
    *,
    project_name: Optional[str],
    project_id: Optional[int] = None,
) -> None:
    if project_name is None:
        return
    charity_project = await charity_project_crud.get_by_attribute(
        "name", project_name, session
    )
    charity_project = charity_project.first()
    if charity_project is not None and charity_project.id != project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def charity_project_id_exist(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Программа не найдена!",
        )
    return charity_project


def check_charity_project_is_closed(charity_project: CharityProject) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def charity_project_permission_to_delete(
    session: AsyncSession,
    *,
    project_id: int,
) -> CharityProject:
    project = await charity_project_id_exist(project_id, session)
    check_charity_project_is_closed(project)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя удалить проект, в который уже были инвестированы "
                "средства, его можно только закрыть."
            ),
        )
    return project


async def check_charity_project_update_blocked(
    session: AsyncSession, *, project_id: int, full_amount: Optional[int]
) -> CharityProject:
    project = await charity_project_id_exist(project_id, session)
    if full_amount is None:
        return project
    check_charity_project_is_closed(project)
    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                "Нельзя установить сумму требуемых инвстиций ниже уже "
                "проинвестированного уровня."
            ),
        )
    return project


def check_data_for_update_in_json(obj):
    dict_obj = obj.dict(exclude_unset=True, exclude_none=True)
    if not dict_obj:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Нет данных для обновления.",
        )
