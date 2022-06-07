from typing import Any, Dict, List

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session:
            AsyncSession
    ) -> List[Dict[str, Any]]:
        """Возвращает все завершенные проекты отсортированные по дате."""
        select_for_test = select(
            [
                extract('year', self.model.close_date) -
                extract('year', self.model.create_date),
                extract('month', self.model.close_date) -
                extract('month', self.model.create_date),
                extract('day', self.model.close_date) -
                extract('day', self.model.create_date)
            ]
        )
        print(type(select_for_test))
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
        objects = await session.execute(select_query)
        return objects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
