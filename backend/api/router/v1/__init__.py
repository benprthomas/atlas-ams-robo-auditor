from fastapi import APIRouter

from .model import model_router
from .cur import cur_router

v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v1_router.include_router(cur_router, prefix="/curs")
v1_router.include_router(model_router, prefix="/models")


__all__ = ["v1_router"]
