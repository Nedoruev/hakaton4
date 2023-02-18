from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from gino import Gino
from data import config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import googlemaps


shelter_chat = '720207278'


BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

db = Gino()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())

scheduler = AsyncIOScheduler()

scheduler.start()

load_dotenv()


data_coordinates = ['48.43582779217483, 35.01247209320486',
                    '47.98997974906745, 34.4532194216179',
                    '48.44268179918284, 35.001667672598124',
                    '48.531453607923645, 35.027680047184404']
API_key = 'AIzaSyARQubWe7FcXv30s4vQkJTy7fLF-m7rVpo'
destinations = data_coordinates
gmaps = googlemaps.Client(key=API_key)


markup_requests = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(KeyboardButton('Найближчі притулки', request_location=True))\
    .add(KeyboardButton('Зворотній зв\'язок', request_contact=True))


contact_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(KeyboardButton('Надіслати власні контакти', request_contact=True))
# markup2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

main_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Знайти друга', callback_data='find_friend')],
    [InlineKeyboardButton('Знайти дім', callback_data='find_shelter')],
    [InlineKeyboardButton('Контакти', callback_data='shelters')]])

kind_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Кіт', callback_data='cat')],
    [InlineKeyboardButton('Собака', callback_data='dog')]])

sex_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Дівчинка', callback_data='girl')],
    [InlineKeyboardButton('Хлопчик', callback_data='boy')]
])

next_pet = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Наступна тварина', callback_data='next_pet')]
])
