from fastapi import FastAPI

from api.v1.users.users import users_v1_api
from api.v1.orders.orders import orders_v1_api

from api.v1.database.access import GetConnectionString  # Доступ к БД
from api.v1.database.manager import DBManager

task3_app = FastAPI()
task3_app.include_router(users_v1_api)
task3_app.include_router(orders_v1_api)


@task3_app.on_event("startup")
def on_startup():
    DBManager.InitializeDB(GetConnectionString())


@task3_app.get("/")
async def index():
    return "It's working!"
