from peewee import *

# Определяем базу данных (SQLite в данном примере)
db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Host(BaseModel):
    # Поле с ID хоста
    ID = CharField()
    # Основное поле hostname
    hostname = CharField()
    # Основное поле IP Address
    IPAddress = CharField()

    speedLimit = IntegerField()
    class Meta:
        table_name = 'hosts'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class Network(BaseModel):
    # Поле с ID сети
    ID = CharField()
    # Поле с именем сети
    name = CharField()
    # Поле с типом сети
    type = CharField()

    isActive = BooleanField()
    class Meta:
        table_name = 'networks'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
class Container(BaseModel):
    # Поле с ID контейнера
    ID = CharField()
    # Поле с ID хоста
    hostID = IntegerField()
    # Поле с именем контейнера
    name = CharField()
    # Поле с названием образа
    image = CharField()

    isActive = BooleanField()

    class Meta:
        table_name = 'containers'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class ContStat(BaseModel):
    # Поле с ID контейнера
    contID = CharField()
    # Поле с загрузкой процессора
    loadCPU = FloatField()
    # Поле с загрузкой оперативной памяти
    loadRAM = FloatField()

    status = CharField()

    lastUpdate = CharField()
    class Meta:
        table_name = 'containerStats'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class NetworkConn(BaseModel):
    # Поле с ID контейнера
    containerID = CharField()
    # Поле с ID сети
    networkID = CharField()
    class Meta:
        table_name = 'netConnection'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class NetworkStatView(BaseModel):
    # Поле с ID контейнера
    rxSpeed = DoubleField()

    txSpeed = DoubleField()

    rxBytes = DoubleField()

    txBytes = DoubleField()
    # Поле с ID сети
    contID = CharField()
    class Meta:
        table_name = 'netStatView'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class NetworkStat(BaseModel):
    lastUpdate = DateTimeField()
    # Поле с ID контейнера
    rxSpeed = DoubleField()

    txSpeed = DoubleField()

    rxBytes = DoubleField()

    txBytes = DoubleField()
    # Поле с ID сети
    contID = CharField()
    class Meta:
        table_name = 'networkStats'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class Agent(BaseModel):
    # Поле с ID контейнера
    name = IntegerField()
    # Поле с UUID
    UUID = TextField()
    # Поле с ID сети
    status = TextField()
    class Meta:
        table_name = 'agents'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class ContView(BaseModel):
    # Поле с ID контейнера
    ContID = CharField()
    # Поле с ID сети
    ContName = CharField()

    HostID = IntegerField()

    loadCPU = DoubleField()

    loadRAM = DoubleField()

    hostname = CharField()

    ContainerStatus = CharField()

    isActive = BooleanField()
    class Meta:
        table_name = 'containerView'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
class ConnView(BaseModel):
    # Поле с ID контейнера
    sourceID = CharField()
    # Поле с ID сети
    targetID = CharField()

    netID = CharField()

    networkName = CharField()

    isActive = BooleanField()
    class Meta:
        table_name = 'linksView'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class ContStatView(BaseModel):
    # Поле с ID контейнера
    ContID = CharField()
    # Поле с ID сети
    lastUpdate = CharField()

    loadCPU = DoubleField()

    loadRAM = DoubleField()

    status = CharField()

    class Meta:
        table_name = 'contStatView'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class Volume(BaseModel):
    # Поле с ID сети
    contID = CharField()

    type = CharField()

    name = CharField()

    class Meta:
        table_name = 'volumes'
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
class Token(BaseModel):
    # Поле с ID сети
    name = CharField()

    token = CharField()

    class Meta:
        table_name = 'tokens'
        primary_key = False
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)