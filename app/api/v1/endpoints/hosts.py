from fastapi import APIRouter, Body
from app.models.schema import agentData, token, hostInfo
from app.core.database import *
from app.core.utils import *
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/hosts", tags=["Hosts"])

@router.post("/updateLimit/")
async def updateLimit(limit: hostInfo):
    if Host.select().where(Host.IPAddress == Host.IPAddress).exists():
        Host.update({Host.limit: limit.limit}).where(Host.IPAddress == Host.IPAddress).execute()
        return {"status": "Ok"}
    return JSONResponse(content={"status": "Bad Token"},status_code=403)