from peewee import *
from app.core.config import Config

config = Config()
# Определяем базу данных (SQLite в данном примере)
db = SqliteDatabase(config.DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

class Group(BaseModel):
    # Поле с ID
    ID = IntegerField(primary_key=True)
    # Основное поле названия
    name = CharField()
    # Основное поле описания
    description = CharField()
    class Meta:
        table_name = 'groups'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class User(BaseModel):
    # Поле с ID пользователя
    ID = IntegerField(primary_key=True)
    # Основное поле имени
    firstName = CharField()
    # Основное поле отчества
    surname = CharField()
    # Основное поле фамилии
    lastName = CharField()
    # Поле с возрастом
    age = IntegerField()
    # Поле с email
    email = CharField()
    # Поле с паролем
    password = CharField()
    # Поле со страной
    countryId = IntegerField()
    # Поле с регионом
    regionId = IntegerField()
    # Поле с городом
    cityId = IntegerField()
    # Поле с уровнем образования
    eduLevelId = CharField()
    # Поле с направлением подготовки
    eduDirection = CharField()
    # Поле с навыками
    softSkills = CharField()
    # Поле с навыками
    hardSkills = CharField()
    # Поле с группой
    groupID = ForeignKeyField(Group, backref='groups', column_name='groupID')
    class Meta:
        table_name = 'users'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
class eduLevel(BaseModel):
    # Поле с ID хоста
    ID = CharField()
    # Основное поле hostname
    name = CharField()
    # Основное поле IP Address
    description = CharField()

    class Meta:
        table_name = 'eduLevel'
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


