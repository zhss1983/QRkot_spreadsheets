from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base import CharityProjectDonationMixin


class CharityProject(CharityProjectDonationMixin, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
