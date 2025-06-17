from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.config import settings
from api.controllers import data_entry_router

app = FastAPI(root_path='/api')


app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOST)

app.include_router(data_entry_router, prefix='/data-entry')
