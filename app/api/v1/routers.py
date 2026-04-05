from fastapi import APIRouter
from .endpoints import agents, containers, netinfo, hosts

router = APIRouter()

router.include_router(router=hosts.router)
router.include_router(router=containers.router)
router.include_router(router=netinfo.router)
router.include_router(router=agents.router)