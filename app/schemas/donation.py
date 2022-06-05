from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, PositiveInt

from .base import DonationCharityProjectDB


class DonationDB(DonationCharityProjectDB):
    user_id: UUID4
    comment: Optional[str] = None


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class DonationShow(DonationCreate):
    id: int
    create_date: Optional[datetime] = None
