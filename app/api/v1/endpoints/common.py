from fastapi import APIRouter, Body, Request
from app.models.schema import user, tokenData, userAuthData
from app.core.database import *
from app.core.utils import *
from uuid import uuid4
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/common", tags=["Common methods"])

@router.get("/eduLevel/")
async def getEduLevel():
    # Проверку на дубликаты
    query = eduLevel.select().execute()
    result = []
    for stat in query:
        result.append({"id": stat.ID,
                       "name": stat.name,
                       "description": stat.description
                       })
    return JSONResponse(content=result,status_code=200)

@router.get("/country/")
async def GetCountry():
    return getCountryList()

@router.get("/region/")
async def GetRegion(ID: int):
    return getRegionByCountry(CountryID=ID)

@router.get("/city/")
async def GetCity(CountID: int, RegID: int):
    return getCityByRegion(CountryID=CountID, RegionID=RegID)
