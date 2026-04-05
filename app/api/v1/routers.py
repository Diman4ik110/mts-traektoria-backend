from fastapi import APIRouter
from .endpoints import admin, auth, career, common

router = APIRouter()

router.include_router(router=common.router)
router.include_router(router=auth.router)
router.include_router(router=admin.router)
router.include_router(router=career.router)