# Понадобится для того, чтобы задать временные интервалы
# Класс «обёртки»

from typing import Any
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
# Создаём экземпляр класса APIRouter
router = APIRouter()

@router.post(
    '/',
    # Тип возвращаемого эндпоинтом ответа
    response_model=list[dict[str, Any]],
    # Определяем зависимости
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        # Начало периода
        # from_reserve: datetime,
        # Конец периода
        # to_reserve: datetime,
        # Сессия
        session: AsyncSession = Depends(get_async_session),
        # «Обёртка»
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    # Получить список проектов.
    # print('--------------------=======================----------------------')
    # print('charity_project_crud.get_projects_by_completion_rate')

    reports = await charity_project_crud.get_projects_by_completion_rate(
        session
    )


    # print('--------------------=======================----------------------')
    # print('spreadsheets_create(wrapper_services)')
    # Создать файл отчёта.
    spreadsheetid = await spreadsheets_create(wrapper_services)
    # print('--------------------=======================----------------------')
    # print('set_user_permissions')
    # Дописать в файл содержимое из БД.
    await set_user_permissions(spreadsheetid, wrapper_services)
    # print('--------------------=======================----------------------')
    # print('spreadsheets_update_value')
    # Вывести данные о файле отчёта.
    await spreadsheets_update_value(spreadsheetid,
                                    reports,
                                    wrapper_services)
    # Стоит вопрос, что вернуть?
    # print('--------------------=======================----------------------')
    return reports
