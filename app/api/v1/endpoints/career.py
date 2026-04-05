from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse, StreamingResponse
from app.models.schema import tokenData
from app.core.database import *
from app.core.utils import *
from app.core.aiRequests import *

router = APIRouter(prefix="/career", tags=["Career"])

# Функция для получения вакансий
@router.get("/showVacancies/")
async def loginUser(token: str):
    try:
        if not token:
            return JSONResponse(content={"message": "Действие запрещено"}, status_code=403)
        # Проверку на дубликаты
        return getCurrentVacancies(token)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# Функция для чата с ИИ
@router.get("/chatWithAI/")
async def chat(message: str):
    return StreamingResponse(
        chatWithAI(message),
        media_type="text/event-stream", # MIME тип для SSE
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

# Функция для генерации траектории
@router.get("/trajectory/")
async def trajectory(token: str):
    return StreamingResponse(
        createTrajectory(token),
        media_type="text/event-stream", # MIME тип для SSE
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Полезно, если за FastAPI стоит nginx, чтобы отключить его буферизацию
            "X-Accel-Buffering": "no",
        }
    )