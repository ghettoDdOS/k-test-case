from fastapi import FastAPI

from api.controllers import data_entry_router

app = FastAPI(root_path='/api')

app.include_router(data_entry_router, prefix='/data-entry')
