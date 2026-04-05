from fastapi import APIRouter, Body, Request
from app.models.schema import agentData, token, uuid
from app.core.database import *
from app.core.utils import *
from uuid import uuid4
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.post("/registerAgent/")
async def registerAgent(agentData: agentData, request: Request = None):
    # Проверку на дубликаты
    if not Agent.select().where(Agent.UUID == agentData.token).exists():
        if Token.select().where(Token.token == agentData.token).exists():
            UUID = uuid4()
            Host.create(
                hostname = agentData.hostname,
                IPAddress = getIPFromRequest(request=request)
            )
            Agent.select()
            Agent.create(
                UUID = UUID,
                status = "Registered",
            )
            return {"authToken": UUID}
        else:
            return JSONResponse(content={"status": "Bad Token"},status_code=403)

@router.post("/checkRegister/")
async def checkRegister(token: token):
    # Проверку на дубликаты
    if not Agent.select().where(Agent.UUID == token.authtoken).exists():
        return JSONResponse(content={"status": "Authorized"},status_code=403)
    return JSONResponse(content={"status": "Authorized"},status_code=200)

@router.put("/unregister/")
async def unregister(data: uuid):
    # Проверку на дубликаты
    Agent.update({"status": "Unregistered"}).where(Agent.UUID == data.UUID).execute()
    return JSONResponse(content={"status": "unregistered"},status_code=200)

@router.delete("/deleteAgent/")
async def deleteAgent(data: uuid):
    # Проверку на дубликаты
    Agent.delete().where(Agent.UUID == data.UUID).execute()
    return JSONResponse(content={"status": "deleted"},status_code=200)

@router.get("/getAgentList/")
async def getAgentList():
    query = Agent.select()
    result = []
    for agent in query:
        result.append({"name": agent.name, 
                       "UUID": agent.UUID,
                       "status": agent.status})
    return result

@router.get("/getTokenList/")
async def getAgentList():
    query = Token.select()
    result = []
    for token in query:
        result.append({"name": token.name, 
                       "id": token.token
                       })
    return result

@router.get("/generateToken/")
async def generateToken():
    Token.create(
        name = "generated",
        token = str(uuid4())
    )
    return JSONResponse(content={"status": "tokenCreated"},status_code=200)

@router.delete("/deleteToken/")
async def deleteToken(token: token):
    # Удаление токена
    Token.delete().where(Token.token == token.token).execute()
    return JSONResponse(content={"status": "deleted"},status_code=200)