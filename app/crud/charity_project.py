from typing import List

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectDB


class CRUDCharityProject(CRUDBase):
    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> List[CharityProjectDB]:
        select_query = (
            select(CharityProject)
            .where(CharityProject.fully_invested)
            .order_by(
                extract("year", CharityProject.close_date)
                - extract("year", CharityProject.create_date),
                extract("month", CharityProject.close_date)
                - extract("month", CharityProject.create_date),
                extract("day", CharityProject.close_date)
                - extract("day", CharityProject.create_date),
                extract("hour", CharityProject.close_date)
                - extract("hour", CharityProject.create_date),
                extract("minute", CharityProject.close_date)
                - extract("minute", CharityProject.create_date),
                extract("second", CharityProject.close_date)
                - extract("second", CharityProject.create_date),
            )
        )
        objects = await session.execute(select_query)
        return objects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
