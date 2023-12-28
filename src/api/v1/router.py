from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .universe import router as universe_router
from .author import router as author_router
from .comics import router as comics_router
from .comics_author import router as comics_author_router
from .character import router as character_router
from .device import router as device_router
from .sweet import router as sweet_router

# Роутер, отвечающий за ветку API версии №1
router = APIRouter(
    prefix="/v1",
    default_response_class=ORJSONResponse
)

# Подключаем роутер вселенной к роутеру V1
router.include_router(router=universe_router)
# Подключаем роутер персонажей к роутеру V1
router.include_router(router=author_router)
# Подключаем роутер комиксов к роутеру V1
router.include_router(router=comics_router)
# Подключаем роутер связи моделей Комикса и Автора к роутеру V1
router.include_router(router=comics_author_router)
# Подключаем роутер персонажа к роутеру V1
router.include_router(router=character_router)
# Подключаем роутер девайса к роутеру V1
router.include_router(router=device_router)
# Подклочаем роутер сладостей к роутеру V1
router.include_router(router=sweet_router)
