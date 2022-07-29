from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from .base import DonationCharityProjectDB


class CharityProjectDB(DonationCharityProjectDB):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

    def __repr__(self):
        return (
            f"{self.name}, {self.description}, {self.id}, {self.full_amount}, "
            f"{self.fully_invested}, {self.create_date}, {self.close_date}"
        )


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None
