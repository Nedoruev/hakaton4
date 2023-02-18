import random
import uuid
# from asyncio.exceptions import
from asyncio import exceptions

import aiogram
from aiogram import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from variables import *
import functions
import asyncio
import asyncpg
from classes import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import link


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # await functions.add_admin(str(uuid.uuid4()), str(720207278))
markup2 = ReplyKeyboardMarkup(resize_keyboard=True)


# @dp.errors_handler(exception=aiogram.utils.exceptions.RetryAfter)
# async def exception_handler(exception: aiogram.utils.exceptions.RetryAfter, id, message, ranges):
#     await send_contacts(id, message, ranges)
#     return True

message1 = 1

@dp.errors_handler(exception=aiogram.utils.exceptions.RetryAfter)
async def exception_handler(update: types.Update, exception: aiogram.utils.exceptions.RetryAfter):
    id = message1.from_user.id
    message1.answer('Тимчасово не працює..')
    ranges = functions.dist(message1.location.latitude, message1.location.longitude)
    await bot.send_contact(id, '+38 (050) 632-34-22', 'Ветеринарна клініка доктора Маковської')
    await message1.answer(f'До притулку *{int(ranges[0] * 1000)}* м', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir//47.9899217,34.453125/@48.1964542,34.4612786,10z')
    await bot.send_contact(id, '+38097 780 3090', 'Притулок для тварин')
    await message1.answer(f'До {link1} *{int(ranges[1] * 1000)}* м\n', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir//48.44242,35.00094/@48.4091676,34.999787,17z')
    await bot.send_contact(id, '067 771 7047', 'Ветеринарна клініка')
    await message1.answer(f'До {link1} *{int(ranges[2] * 1000)}* м', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir/48.3908544,35.004025/48.53325,35.0281/@48.46231,34.9702349,12z/data=!3m1!4b1!4m4!4m3!1m1!4e1!1m0')
    await bot.send_contact(id, '068 828 2255', 'Притулок для тварин')
    await message1.answer(f'До {link1} *{int(ranges[3] * 1000)}* м', parse_mode='Markdown')
    return True


async def startup_database():
    print('устанавливается связь с базой данных')
    await db.set_bind(config.POSTGRES_URI)


@dp.callback_query_handler(lambda call: 'find_shelter' in call.data, state=None)
async def find_shelters(call):
    await FSM.photo.set()
    print(call)
    await bot.send_message(call.from_user.id, 'Будь-ласка надішліть фото тварини')


@dp.message_handler(content_types=['photo'], state=FSM.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.photo[-1].download(f'C:\\Users\dixoc\Desktop\hackathon\hackathon2\\{data["photo"]}.png')
    await FSM.next()
    await message.reply('Будь ласка вкажіть місто, де була знайдена тварина')


@dp.message_handler(state=FSM.city)
async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await FSM.next()
    await message.reply('Оберіть вид тварини🐱🐶', reply_markup=kind_menu)


@dp.callback_query_handler(lambda call: 'cat' in call.data, state=FSM.kind)
async def load_kind1(call, state: FSMContext):
    async with state.proxy() as data:
        data['kind'] = 'Кіт'
    await FSM.next()
    await functions.edit_message(call.message, 'Оберіть стать')
    await call.message.edit_reply_markup(sex_menu)


@dp.callback_query_handler(lambda call: 'dog' in call.data, state=FSM.kind)
async def load_kind2(call, state: FSMContext):
    async with state.proxy() as data:
        data['kind'] = 'Собака'
    await FSM.next()
    await functions.edit_message(call.message, 'Оберіть стать')
    await call.message.edit_reply_markup(sex_menu)
    # await bot.send_message(call.from_user.id, 'Оберіть стать', reply_markup=sex_menu)


@dp.callback_query_handler(lambda call: 'girl' in call.data, state=FSM.sex)
async def load_kex(call, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = 'Дівчинка'
    await FSM.next()
    await functions.edit_message(call.message, 'Будь ласка вкажіть породу тварини')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(lambda call: 'find_friend' in call.data)
async def find_friend(call):
    pets = random.choice(await functions.select_all_pets())
    with open(pets.photo, 'rb') as photo:
        await bot.send_photo(call.from_user.id, photo=photo, caption=f'*Місто*: {pets.city}\n'
                                                                     f'*Це* - {pets.kind}\n'
                                                                     f'*Стать*: {pets.sex}\n'
                                                                     f'*Порода:*: {pets.breed}\n'
                                                                     f'*Контактний номер:*: {pets.contact[:12:]}\n'
                                                                     f'*Контактна людина:*: {pets.contact[12::]}')


@dp.callback_query_handler(lambda call: 'boy' in call.data, state=FSM.sex)
async def load_kinsex1(call, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = 'Хлопчик'
    await FSM.next()
    await functions.edit_message(call.message, 'Будь ласка вкажіть породу тварини')
    await call.message.edit_reply_markup()


@dp.message_handler(state=FSM.breed)
async def load_breed(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['breed'] = message.text
    await FSM.next()
    await message.answer('Останній крок😌: Надішліть свої контакти,'
                         ' скориставшись кнопкою нижче,'
                         ' або за потреби надішліть контакт іншої людини'
                         'надішліть інший контакт', reply_markup=contact_request)


@dp.message_handler(content_types=['contact'], state=FSM.contact)
async def load_breed(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = (message.contact.phone_number, message.contact.first_name)
    async with state.proxy() as data:
        with open(f"C:\\Users\dixoc\Desktop\hackathon\hackathon2\\{data['photo']}.png", 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo, caption=f'*Місто*: {data["city"]}\n'
                                                                      f'*Вид*: {data["kind"]}\n'
                                                                      f'*Стать*: {data["sex"]}\n'
                                                                      f'*Порода*: {data["breed"]}\n'
                                                                      f'*Контактний номер*: {data["contact"][0]}\n'
                                                                      f'*Контактне ім\'я*: {data["contact"][1]}', parse_mode='Markdown')
            await functions.add_finded_pet(f"C:\\Users\dixoc\Desktop\hackathon\hackathon2\\{data['photo']}.png",
                                           data["city"], data['kind'], data['sex'], data['breed'],
                                           ''.join(data['contact']))
            # for admin in await functions.select_all_admins():
            #     await bot.send_photo(int(admin.id), photo, caption=f'*Місто*: {data["city"]}\n'
            #                                                               f'*Вид*: {data["kind"]}\n'
            #                                                               f'*Стать*: {data["sex"]}\n'
            #                                                               f'*Порода*: {data["breed"]}\n'
            #                                                               f'*Контактний номер*: {data["contact"][0]}\n'
            #                                                               f'*Контактне ім\'я*: {data["contact"][1]}',
            #                      parse_mode='Markdown')
        # await message.reply()
        os.remove(f"C:\\Users\dixoc\Desktop\hackathon\hackathon2\\{data['photo']}.png")
    await state.finish()


@dp.callback_query_handler(lambda call: 'shelters' in call.data)
async def load_kinsex1(call):
    await bot.send_message(call.from_user.id, 'Перегляньте найближчі до вас притулки,'
                                              ' або замовте зворотній дзвінок за допомогою'
                                              ' кнопки нижче📲',
                           reply_markup=markup_requests)


@dp.message_handler(text='/start')
async def starting(message: types.Message):
    await message.answer(f'Чим Вам допомогти?☺️', reply_markup=main_menu)


@dp.message_handler(content_types=['location'])
async def start(message: types.Message):
    id = message.from_user.id
    global message1
    message1 = message
    # await message.answer('Тимчасово не працює..')
    ranges = functions.dist(message.location.latitude, message.location.longitude)
    # await message.answer('123')
    await bot.send_contact(id, '+38 (050) 632-34-22', 'Ветеринарна клініка доктора Маковської')
    await message.answer(f'До притулку *{int(ranges[0] * 1000)}* м', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir//47.9899217,34.453125/@48.1964542,34.4612786,10z')
    await bot.send_contact(id, '+38097 780 3090', 'Притулок для тварин')
    await message.answer(f'До {link1} *{int(ranges[1] * 1000)}* м\n', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir//48.44242,35.00094/@48.4091676,34.999787,17z')
    await bot.send_contact(id, '067 771 7047', 'Ветеринарна клініка')
    await message.answer(f'До {link1} *{int(ranges[2] * 1000)}* м', parse_mode='Markdown')
    link1 = link('притулку',
                 'https://www.google.com/maps/dir/48.3908544,35.004025/48.53325,35.0281/@48.46231,34.9702349,12z/data=!3m1!4b1!4m4!4m3!1m1!4e1!1m0')
    await bot.send_contact(id, '068 828 2255', 'Притулок для тварин')
    await message.answer(f'До {link1} *{int(ranges[3] * 1000)}* м', parse_mode='Markdown')
    # try:
    #     await send_contacts(id, message, ranges)
    # except Exception as ex:
    #     await exception_handler(exception=ex, id=id, message=message, ranges=ranges)


@dp.message_handler(content_types=['contact'])
async def remove(message: types.Message):
    await message.answer(f'Дякуємо за звернення!🤗 Найближчим часом з Вами зв\'яжеться менеджер за даними:\n'
                         f'*Номер*: {message.contact.phone_number}\n'
                         f'*Ім\'я*: {message.contact.first_name}', parse_mode='Markdown',
                         reply_markup=ReplyKeyboardRemove())


async def on_startup(dp: dp):
    await functions.set_default_commands(dp)
    print('бот запущен')


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database=config.DATABASE,
    user=config.PGUSER,
    password=config.PGPASSWORD,
    max_inactive_connection_lifetime=100)


loop = asyncio.get_event_loop()
loop.run_until_complete(db2_test())


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as ex:
        print(ex)
        executor.start_polling(dp, on_startup=on_startup)
