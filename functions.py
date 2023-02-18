from asyncpg import UniqueViolationError

from classes import *
from uuid import uuid4


def dist(x,y):
    latitude= float(x)
    longtitude= float(y)
    origin = (latitude, longtitude)
    actual_distance_car= []
    for destination in destinations:
        result = gmaps.distance_matrix(origin, destination,
                                       mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
        result = result / 1000
        actual_distance_car.append(result)
    return actual_distance_car

# dist(input(''), input(''))


async def set_default_commands(dp: dp):
    await dp.bot.set_my_commands([
        types.BotCommand('/start', 'Розпочати'),
    ])


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)


async def edit_message(message: types.Message, text):
    new_mess = await message.edit_text(text, parse_mode='Markdown')
    return new_mess


def create_uuid():
    return str(uuid4())


# async def startup_database(disptcher: dp):
#     print('устанавливается связь с базой данных')
#     await db.set_bind(config.POSTGRES_URI)
#
#
# async def select_all_pets():
#     pets = await Pet.query.gino.all()
#     return pets


async def select_all_admins():
    admins = await Admins.query.gino.all()
    return admins


async def select_all_pets():
    admins = await Finded_Pets.query.gino.all()
    return admins
# async def select_all_users():
#     users = await User.query.gino.all()
#     return users
#
#
# async def select_all_disc():
#     disc = await Lessons.query.gino.all()
#     return disc
#
#
# async def select_disc(less_name):
#     disc = await Lessons.query.where(Lessons.less_name == less_name).gino.first()
#     return disc
#
#
# async def update_disc_name(disc, name):
#     await disc.update(less_name=name).apply()
#
#
# async def select_user_by_id(user_id: int):
#     user = await User.query.where(User.user_id == user_id).gino.first()
#     return user
#
#
# async def select_user_by_token(token):
#     user = await User.query.where(User.token == token).gino.first()
#     return user
#
#
# async def select_user(name):
#     user = await User.query.where(User.name == name).gino.first()
#     return user
#
#
# async def select_by_role(role):
#     user = await User.query.where(User.role == role).gino.first()
#     return user
#
#
# async def change_password(password: str, token: str):
#     user = await select_user_by_token(token)
#     await user.update(password=password).apply()
#
#
# async def update_user_id(user, user_id):
#     await user.update(user_id=user_id).apply()
#
#
# async def update_user_name(user, name):
#     await user.update(name=name).apply()
#
#
# async def update_user_disc(user, disc):
#     await user.update(disc=disc).apply()
#
#
# async def disc_info(disc):
#     return disc.info.split(' / ')[0]


# async def update_disc_info(disc, info):
#     studetns = disc.info.split(' / ')[1]
#     new_info = info + ' / ' + studetns
#     await disc.update(info=new_info).apply()


async def add_admin(token, id):
    try:
        admin = Admins(id=id, token=token)
        await admin.create()
    except UniqueViolationError:
        pass


async def add_finded_pet(photo, city, kind, sex, breed, contact):
    try:
        pet = Finded_Pets(photo=photo, city=city, kind=kind, sex=sex, breed=breed, contact=contact)
        await pet.create()
    except UniqueViolationError:
        pass



