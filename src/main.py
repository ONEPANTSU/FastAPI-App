import aioredis as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead
from src.config import CACHE_HOST, CACHE_PORT
from src.operations.router import router as router_operations
from src.tasks.router import router as router_report

logger.add(
    "../app.log",
    format="{time}\t|\t{level}\t|\t{message}",
    level="INFO",
    rotation="10MB",
    compression="zip",
)

app = FastAPI(title="Trading App")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operations)
app.include_router(router_report)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{CACHE_HOST}:{CACHE_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
