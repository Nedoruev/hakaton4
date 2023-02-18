from typing import List
import sqlalchemy
import datetime
import sqlalchemy as sa
from aiogram.dispatcher.filters.state import StatesGroup, State
from variables import *


class FSM(StatesGroup):
    photo = State()
    city = State()
    kind = State()
    sex = State()
    breed = State()
    contact = State()


# class FSMAdmin(StatesGroup):
#     photo = State()
#     city = State()
#     kind = State()
#     sex = State()
#     breed = State()
#     contact = State()



class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),)


class Admins(TimedBaseModel):
    __tablename__ = 'admins'
    token = sa.Column(sa.String(200), primary_key=True)
    id = sa.Column(sa.String(200), primary_key=True)
    query: sqlalchemy.select


class Finded_Pets(TimedBaseModel):
    __tablename__ = 'finded_pets'
    photo = sa.Column(sa.String(200), primary_key=True)
    city = sa.Column(sa.String(200), primary_key=True)
    kind = sa.Column(sa.String(200), primary_key=True)
    sex = sa.Column(sa.String(200), primary_key=True)
    breed = sa.Column(sa.String(200), primary_key=True)
    contact = sa.Column(sa.String(200), primary_key=True)
    query: sqlalchemy.select


# class Pets(TimedBaseModel):
#     __tablename__ = 'pets'
#     photo = sa.Column(sa.String(200), primary_key=True)
#     city = sa.Column(sa.String(200), primary_key=True)
#     kind = sa.Column(sa.String(200), primary_key=True)
#     sex = sa.Column(sa.String(200), primary_key=True)
#     breed = sa.Column(sa.String(200), primary_key=True)
#     contact = sa.Column(sa.String(200), primary_key=True)
#     breed = sa.Column(sa.String(200), primary_key=True)
#     contact = sa.Column(sa.String(200), primary_key=True)
#     query: sqlalchemy.select