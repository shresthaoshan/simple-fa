from fastapi import FastAPI
from db.core import init_db
from routers import api

app  = FastAPI()

init_db()

app.include_router(api.router)