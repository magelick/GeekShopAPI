from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .v1.router import router as v1_router

# Роутер, отвечающий за ветку API целеком
router = APIRouter(
    prefix="/api",
    default_response_class=ORJSONResponse
)

# Подключаем роутер V1 к основному роутеру API
router.include_router(router=v1_router)