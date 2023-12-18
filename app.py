from fastapi import FastAPI
from src.api.router import router as api_router

# Самый главный роутер
app = FastAPI(
    title="API Гиг-Магазина"
)
# Подключаем к самому главному роутеру роутер API
app.include_router(router=api_router)
