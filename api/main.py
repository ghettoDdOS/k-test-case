from collections.abc import MutableMapping
from os import PathLike
from typing import Any, override

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from api.config import settings
from api.controllers import data_entry_router

app = FastAPI()


app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOST)

api_router = APIRouter()

api_router.include_router(data_entry_router, prefix='/data-entry')


class SPA(StaticFiles):
    def __init__(
        self,
        *,
        directory: str | PathLike[str],
        check_dir: bool = True,
        follow_symlink: bool = False,
    ) -> None:
        super().__init__(
            directory=directory,
            packages=None,
            html=True,
            check_dir=check_dir,
            follow_symlink=follow_symlink,
        )

    @override
    async def get_response(
        self, path: str, scope: MutableMapping[str, Any]
    ) -> Response:
        try:
            response = await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as exc:
            if exc.status_code == status.HTTP_404_NOT_FOUND:
                return await super().get_response('.', scope)
            raise
        else:
            return response


app.include_router(api_router, prefix='/api')
app.mount('/', SPA(directory='dist'), name='app')
