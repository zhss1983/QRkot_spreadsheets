from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import not_, select
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserDB


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalar()

    async def refresh(self, db_obj, session: AsyncSession):
        await session.refresh(db_obj)
        return db_obj

    async def get_multi(self, session: AsyncSession):
        db_obj = await session.execute(select(self.model))
        return db_obj.scalars().all()

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> ScalarResult:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(select(self.model).where(attr == attr_value))
        return db_obj.scalars()

    def get_object_from_dict(self, obj_in, user: Optional[UserDB] = None):
        in_data = obj_in.dict(exclude_unset=True, exclude_none=True)
        in_data["invested_amount"] = 0
        if user is not None:
            in_data["user_id"] = user.id
        obj = self.model(**in_data)
        return obj

    async def create(
        self,
        db_obj,
        session: AsyncSession,
    ):
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if obj_data is None:
            print(jsonable_encoder(db_obj))
            print(obj_in.dict())

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_multi(self, list_db, session: AsyncSession):
        session.add_all(list_db)
        await session.commit()

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_active(self, session: AsyncSession) -> ScalarResult:
        select_task = (
            select(self.model)
            .where(not_(self.model.fully_invested))
            .order_by(self.model.create_date.asc())
        )
        return await session.scalars(select_task)
