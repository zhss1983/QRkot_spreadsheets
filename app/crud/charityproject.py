from typing import Any, Optional, Union
from sqlalchemy import not_, select, func

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from app.crud.base import CRUDBase

from fastapi.encoders import jsonable_encoder
from pprint import pprint

class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session:
            AsyncSession
    ) -> list[dict[str, Any]]:
        """Возвращает все завершенные проекты отсортированные по дате."""
        # print(
        #     '--------------------=======================----------------------')
        # print(
        #     'select_query = select(')
        select_query = select(
            [
                self.model.name,
                self.model.description,
                self.model.close_date,
                self.model.create_date
            ]
        ).where(
            self.model.fully_invested
        )
        # print('--------------------=======================----------------------')
        # print('objects = await session.execute(select_query)')
        objects = await session.execute(select_query)
        objects = objects.all()
        # print('--------------------=======================----------------------')
        # pprint(jsonable_encoder(objects))
        # print('--------------------=======================----------------------')
        return objects


charity_project_crud = CRUDCharityProject(CharityProject)
