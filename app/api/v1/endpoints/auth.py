from fastapi import APIRouter, Body, Request
from app.models.schema import user, tokenData, userAuthData, updateUser
from app.core.database import *
from app.core.utils import *
from app.core.encryption import *
from fastapi.responses import JSONResponse
import hashlib
from playhouse.shortcuts import model_to_dict

router = APIRouter(prefix="/auth", tags=["Auth"])

# Маршрут для авторизации
@router.post("/login/")
async def loginUser(userData: userAuthData):
    try:
        if User.select().where((User.email == userData.email) & (User.password == hashlib.sha256((userData.password).encode("utf-8")).hexdigest())).exists():
            payload = model_to_dict(User.get(User.email == userData.email))
            return JSONResponse(content={"token": generateJWTToken(payload=payload)})
        else:
            return JSONResponse(content={"status": "Wrong email or password"},status_code=403)
    except Exception as e:
        return JSONResponse(content={"status": e },status_code=500)
# Маршрут для изменения пароля
@router.get("/updatePassword/")
async def updatePassword(newPassword: str, token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        User.update(
                password = hashlib.sha256((newPassword).encode("utf-8")).hexdigest()
            ).where(User.ID == decodeJWTToken(token.token)['id']).execute()
        return JSONResponse(content={ "status": "Password updated" }, status_code=200)
    except Exception as e:
        return JSONResponse(content={ "status": e }, status_code=500)
# Маршрут для регистрации
@router.post("/register/")
async def registerUser(userData: user):
    try:
        # Проверку на дубликаты
        if not User.select().where(User.email == userData.email & User.password == hashlib.sha256((userData.password).encode("utf-8")).hexdigest()).exists():
            User.create(
                firstName = userData.firstName,
                surname = userData.surname,
                lastName = userData.lastName,
                age = userData.age,
                email = userData.email,
                password = hashlib.sha256((userData.password).encode("utf-8")).hexdigest(),
                countryId = userData.countryId,
                regionId = userData.regionId,
                cityId = userData.cityId,
                eduLevelId = userData.eduLevelId,
                eduDirection = userData.eduDirection,
                softSkills = userData.softSkills,
                hardSkills = userData.hardSkills,
            ).save()
            return JSONResponse(content={"status": "Registered"},status_code=200)
        return JSONResponse(content={"status": "User already registered"},status_code=403)
    except Exception as e:
        return JSONResponse(content={"status": e },status_code=500)

# Маршрут для валидации токена
@router.post("/checkLogin/")
async def checkLogin(token: tokenData):
    # Валидация токена
    if isJWTTokenValid(token.token):
        return JSONResponse(content={"status": "logged"},status_code=200)
    return JSONResponse(content={"status": "Access denied"},status_code=403)

# Маршрут для удаления пользователя
@router.post("/deleteUser/")
async def unregister(token: tokenData):
    try:
        # Валидация токена
        if not isJWTTokenValid(token.token):
            return JSONResponse(content={"status": "Access denied"},status_code=403)
        # Удаление пользователя
        if User.select().where(User.id == decodeJWTToken(token.token)['id']).exists():
            User.delete().where(User.id == decodeJWTToken(token.token)['id']).execute()
        return JSONResponse(content={"status": "unregistered"},status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e },status_code=500)

# Маршрут для получения данных пользователя
@router.get("/userData/")
async def getUserData(token: str):
    try:
        # Валидация токена
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Access denied"},status_code=403)
        userData = User.select(User.firstName, User.surname, User.lastName, User.age, User.email, User.countryId, User.regionId, User.cityId, User.eduLevelId, User.eduDirection, User.softSkills, User.hardSkills).where(User.ID == decodeJWTToken(token)['ID']).get()
        return JSONResponse(content=model_to_dict(userData),status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e },status_code=500)

# Маршрут для обновления данных пользователя
@router.post("/updateUser/")
async def updateUser(token: tokenData, newData: updateUser ):
    try:
        print(token.token)
        # Валидация токена
        if not isJWTTokenValid(token.token):
            return JSONResponse(content={"status": "Access denied"},status_code=403)
        # Проверку на дубликаты
        if User.select().where(User.ID == decodeJWTToken(token=token.token)['ID']).exists():
            updatedUser = User.update(
                firstName = newData.firstName,
                surname = newData.surname,
                lastName = newData.lastName,
                age = newData.age,
                email = newData.email,
                countryId = newData.countryId,
                regionId = newData.regionId,
                cityId = newData.cityId,
                eduLevelId = newData.eduLevelId,
                eduDirection = newData.eduDirection,
                softSkills = newData.softSkills,
                hardSkills = newData.hardSkills,
            ).where(User.ID == decodeJWTToken(token=token.token)['ID']).execute()

            return JSONResponse(content={"status": "success"},status_code=200)
        return JSONResponse(content={"status": "User not found"},status_code=403)
    except Exception as e:
        return JSONResponse(content={"status": e },status_code=500)