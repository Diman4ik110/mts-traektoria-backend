from pydantic import BaseModel

# Класс который будет использоваться для валидации данных о виртуальных машинах
class hostInfo(BaseModel):
    hostname: str
    IPAddress: str
    netLimit: int
# Класс который будет использоваться для валидации данных о контейнерах
class contrainerInfo(BaseModel):
    name: str
    id: str
    hostname: str
    image: str

# Класс который будет использоваться для валидации метрик
class contMetrics(BaseModel):
    contID: str
    lastUpdate: str
    loadCPU: float
    loadRAM: float
    status: str

# Класс который будет использоваться для валидации данных о сетях к которым подключены контейнеры
class networkList(BaseModel):
    netID: str
    name: str

# Класс который будет использоваться для валидации данных о подключениях между контейнерами
class networkConnection(BaseModel):
    netID: str
    contID: str
# Класс который будет использоваться для валидации данных о подключениях между контейнерами
class networkStat(BaseModel):
    lastUpdate: str
    # Поле с ID контейнера
    rxSpeed: float

    txSpeed: float

    rxBytes: int

    txBytes: int
    # Поле с ID сети
    contID: str
    
# Класс который будет использоваться для валидации данных регистрации агентов
class agentData(BaseModel):
    token: str
    IPAddress: str

# Класс который будет использоваться для валидации токена агента
class agentData(BaseModel):
    token: str
    hostname: str
    
# Класс который будет использоваться для валидации токена агента
class token(BaseModel):
    authtoken: str

# Класс который будет использоваться для валидации информации о volume
class volumeData(BaseModel):
    contID: str
    name: str
    type: str
    size: float

class contID(BaseModel):
    contID: str

class connID(BaseModel):
    connID: str

class uuid(BaseModel):
    UUID: str