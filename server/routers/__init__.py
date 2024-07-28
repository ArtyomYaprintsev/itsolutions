from fastapi import APIRouter

from .ads import router as ad_router
from .users import router as user_router
from .auth import router as auth_router

router = APIRouter()

router.include_router(ad_router, prefix='/ads', tags=['ads'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(user_router, prefix='/users', tags=['users'])
