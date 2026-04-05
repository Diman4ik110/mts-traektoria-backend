from fastapi import APIRouter, Body
from app.models.schema import volumeData
from app.core.database import *
from uuid import uuid4

router = APIRouter(prefix="/volumes", tags=["Volumes"])

@router.post("/sendVolume/")
async def sendVolume(volume: volumeData = Body(...)):
    # Проверку на дубликаты
    if not Volume.select().where(Volume.ID == volume.name).exists():
        Volume.create(
            contID=volumeData.contID,
            name=volumeData.name,
            size=volumeData.size,
            type=volumeData.type
        )
    return {"status": "success"}