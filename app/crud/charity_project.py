from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectInvestedDB


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self, session: AsyncSession
    ) -> List[CharityProjectInvestedDB]:
        select_query = select(
            [
                CharityProject.name,
                CharityProject.description,
                CharityProject.close_date,
                CharityProject.create_date
            ]
        ).where(
            CharityProject.fully_invested
        )
        objects = await session.execute(select_query)
        return objects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
