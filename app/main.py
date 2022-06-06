from fastapi import FastAPI

from app.api.routers import main_router as router
from app.core.init_db import create_first_superuser

if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv
    from app.core.config import Settings
    from pprint import pprint

    load_dotenv()
    
    settings = Settings()
    for attr in settings.__dict__:
        first = attr[0]
        if first != first.upper():
            try:
                new_attr = getenv(attr.upper())
                settings.__setattr__(attr, new_attr)
                # pprint(f'{attr}: {new_attr}')
            except Exception as E:
                pprint(E)
                pass
else:
    from app.core.config import settings

app = FastAPI(config=settings, title=settings.app_title)
app.include_router(router)

@app.on_event('startup')
async def startup():
    await create_first_superuser()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app.main:app', reload=True)
