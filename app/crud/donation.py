from app.models import Donation

from .base import CRUDBase


class CRUDDonation(CRUDBase):
    pass


donation_crud = CRUDDonation(Donation)
