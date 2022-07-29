from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import Column, ForeignKey, Text

from app.core.db import Base

from .base import CharityProjectDonationMixin


class Donation(CharityProjectDonationMixin, Base):
    user_id = Column(GUID, ForeignKey("user.id"))
    comment = Column(Text, nullable=True)
