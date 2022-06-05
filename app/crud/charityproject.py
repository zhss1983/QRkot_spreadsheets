from app.models import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    pass


charity_project_crud = CRUDCharityProject(CharityProject)
