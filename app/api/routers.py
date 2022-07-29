from fastapi import APIRouter

from app.api.endpoints import (
    charityproject_router,
    donation_router,
    google_api_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    charityproject_router, prefix="/charity_project", tags=["Charity Projects"]
)
main_router.include_router(donation_router, prefix="/donation", tags=["Donations"])
main_router.include_router(google_api_router, prefix="/google", tags=["Google"])
main_router.include_router(user_router)
