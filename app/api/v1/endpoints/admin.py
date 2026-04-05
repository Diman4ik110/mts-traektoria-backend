from fastapi import APIRouter, Body, Request
from app.core.database import *
from app.core.utils import *
from fastapi.responses import JSONResponse
from playhouse.shortcuts import model_to_dict
from app.models.schema import *
from app.core.encryption import isJWTTokenValid, decodeJWTToken

router = APIRouter(prefix="/admin", tags=["Administration"])

# Маршрут для получения списка пользователей
@router.get("/listUsers/")
async def listUsers(token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        # Проверка, что пользователь принадлежит к группе admin
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        users = User.select().join(Group, on=(User.groupID == Group.ID)).execute()
        usersList = [model_to_dict(user) for user in users]
        return JSONResponse(content=usersList, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)

# Маршрут для обновления данных пользователя
@router.post("/updateUser/")
async def updateUser(userData: adminUserData, newUserData: user):
    try:
        print(userData.ID)
        if not isJWTTokenValid(userData.token.token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        User.update(
                firstName = newUserData.firstName,
                surname = newUserData.surname,
                lastName = newUserData.lastName,
                age = newUserData.age,
                email = newUserData.email,
                countryId = newUserData.countryId,
                regionId = newUserData.regionId,
                cityId = newUserData.cityId,
                eduLevelId = newUserData.eduLevelId,
                eduDirection = newUserData.eduDirection,
                softSkills = newUserData.softSkills,
                hardSkills = newUserData.hardSkills,
            ).where(User.ID == userData.ID).execute()
        return JSONResponse(content={"status": "User updated"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)

# Маршрут для изменения пароля пользователя
@router.get("/changeUserPassword/")
async def changeUserPassword(newPassword: str, userID: int, token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        # Проверка, что пользователь принадлежит к группе admin
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        User.update(
                password = hashlib.sha256((newPassword).encode("utf-8")).hexdigest()
            ).where(User.ID == userID).execute()
        return JSONResponse(content=groupList, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)

# Маршрут для получения списка групп
@router.get("/listGroups/")
async def listGroups(token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        # Проверка, что пользователь принадлежит к группе admin
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        groups = Group.select(Group.name, Group.description).execute()
        groupList = [model_to_dict(group) for group in groups]
        return JSONResponse(content=groupList, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)

# Маршрут для создания группы
@router.post("/newGroup/")
async def newGroup(groupData: group, token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        Group.create(
            name=groupData.name,
            description=groupData.description
            ).save()
        return JSONResponse(content={"status": "Group created"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)



# Маршрут для удаления группы
@router.delete("/deleteGroup/")
async def deleteGroup(groupData: group, token: str):
    try:
        if not isJWTTokenValid(token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        if not Group.select().where(Group.name == groupData.name).exists():
            return JSONResponse(content={"status": "Group does not exist"}, status_code=404)
        if Group.delete().where(Group.name == groupData.name).execute():
            return JSONResponse(content={"status": "Group deleted"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)

# Маршрут для удаления пользователя
@router.delete("/deleteUser/")
async def deleteUser(userData: adminUserData):
    try:
        if not isJWTTokenValid(userDeleteData.token):
            return JSONResponse(content={"status": "Invalid token"}, status_code=403)
        user = User.select().join(Group, on=(User.groupID == Group.ID)).where(User.ID == decodeJWTToken(token)['ID']).execute()
        if not user[0].groupID.name == "admins":
            return JSONResponse(content={"status": "User does not have permission"}, status_code=403)
        if User.delete().where(User.id == decodeJWTToken(userDeleteData.token)['id']).execute():
            return JSONResponse(content={"status": "User deleted"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": e }, status_code=500)