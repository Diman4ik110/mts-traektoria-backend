from typing import Dict, Any, Optional
import json
from typing import AsyncGenerator
from playhouse.shortcuts import model_to_dict
import openai
import asyncio
from app.core.database import *
from app.core.encryption import decodeJWTToken
from app.core.config import Config


config = Config()
# Инициализируем клиента OpenAI, но перенаправляем его на локальный сервер
client = openai.OpenAI(
    base_url=config.LLM_ENDPOINT,
    api_key=config.LLM_API_KEY,
)

async def chatWithAI(prompt: str):
    """Асинхронный генератор, который вызывает синхронный OpenAI в потоке"""
    try:
        # Важно: Запускаем синхронный генератор в отдельном потоке
        def sync_generate():
            return client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.7,
            )
        
        # Запускаем синхронный код в потоке
        stream = await asyncio.to_thread(sync_generate)
        
        # Но сам stream уже итерируемый, итерация тоже может блокировать
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'data': content})}\n\n"
            await asyncio.sleep(0)  # Даём шанс event loop'у
            
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

async def createTrajectory(token: str):
    """Асинхронный генератор, который вызывает синхронный OpenAI в потоке"""
    try:
        userData = model_to_dict(User.select(User.age, 
                                             User.eduDirection, 
                                             User.softSkills, 
                                             User.hardSkills).where(User.ID == decodeJWTToken(token)['ID']).get())
        prompt = f"""
            Ты эксперт по планированию карьеры. Создай траекторию карьеры для пользователя. Укажи в этапах какие технологии необходимо изучить, а также список курсов, которые нужно можно пройти для освоения данной технологии. 
            Имеется информация о пользователе: {userData}. Сделай без упоминания пользователя и можешь увеличить количество этапов.
            Необходимо сгенерировать траекторию карьеры в формате JSON. Формат показан ниже:
            "title": "Trajectory Stages",
            "type": "object",
            "stages': 
                "stage1": 
                    "name": "string",
                    "description": "string"
                    "courses":
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                "stage2": 
                    "name": "string",
                    "description": "string"
                    "courses":
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                "stage3": 
                    "name": "string",
                    "description": "string"
                    "courses":
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
                        "course":
                            "name": "string",
                            "description": "string"
                            "link": "string"
        """
        # Важно: Запускаем синхронный генератор в отдельном потоке
        def sync_generate():
            return client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.7,
            )
        
        # Запускаем синхронный код в потоке
        stream = await asyncio.to_thread(sync_generate)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'data': content})}\n\n"
            await asyncio.sleep(0)  # Даём шанс event loop'у
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"