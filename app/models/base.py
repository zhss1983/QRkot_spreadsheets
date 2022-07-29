from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class CharityProjectDonationMixin:
    @declared_attr
    def full_amount(cls):
        return Column(Integer)

    @declared_attr
    def invested_amount(cls):
        return Column(Integer, default=0)

    @declared_attr
    def fully_invested(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def create_date(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def close_date(cls):
        return Column(DateTime())

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint("full_amount >= 0", name="check_full_amount_positive"),
            CheckConstraint(
                "invested_amount >= 0", name="check_invested_amount_positive"
            ),
        )
