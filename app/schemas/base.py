from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCharityProjectDB(BaseModel):
    id: int
    full_amount: int = Field(..., gte=0)
    invested_amount: int = Field(..., gte=0)
    fully_invested: bool = False
    create_date: Optional[datetime] = None
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
