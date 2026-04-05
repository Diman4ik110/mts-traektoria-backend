from pydantic import BaseModel

# Класс который будет использоваться для валидации данных о пользователе
class user(BaseModel):
    firstName: str
    surname: str
    lastName: str
    age: int
    email: str
    password: str
    countryId: int
    regionId: int
    cityId: int
    eduLevelId: str
    eduDirection: str
    softSkills: str
    hardSkills: str

# Класс который будет использоваться для валидации токена
class tokenData(BaseModel):
    token: str

# Класс который будет использоваться для валидации данных о пользователе
class userAuthData(BaseModel):
    # Основное поле hostname
    email: str
    # Основное поле IP Address
    password: str

class group(BaseModel):
    name: str
    description: str

class adminUserData(BaseModel):
    ID: int
    token: tokenData

# Класс который будет использоваться для валидации данных о пользователе
class updateUser(BaseModel):
    firstName: str
    surname: str
    lastName: str
    age: int
    email: str
    countryId: int
    regionId: int
    cityId: int
    eduLevelId: str
    eduDirection: str
    softSkills: str
    hardSkills: str