from fastapi import FastAPI

from app.api.routers import main_router as router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(config=settings, title=settings.app_title)
app.include_router(router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
