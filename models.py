from peewee import *

db = SqliteDatabase('Cozzy.db')

class BaseModel(Model):
    class Meta:
        database = db

class Country(BaseModel):
    id = AutoField(),
    name = CharField(unique=True)

class City(BaseModel):
    id = AutoField(),
    name = CharField(unique=True)
    
class Space(BaseModel):
    id = AutoField(),
    name = CharField()
    city = ForeignKeyField(City, backref='spaces')
    country = ForeignKeyField(Country, backref='spaces')
    address = CharField()
    phone = CharField()
    mapUrl = CharField()
    price = IntegerField()
    rating = IntegerField()
    thumbnail = CharField()
    kitchens = IntegerField()
    bedrooms = IntegerField()
    closets = IntegerField()

class SpacePhoto(BaseModel):
    id = AutoField(),
    space = ForeignKeyField(Space, backref='photos')
    photo = CharField()


def create_tables():
    with db:
        db.create_tables([Country, City, Space, SpacePhoto])