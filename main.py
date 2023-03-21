import asyncio
import random # импортируем модуль random
from aiogram import Bot, types, Dispatcher  # библиотека для работы с телеграмм ботами
from aiogram.utils import executor

from config import *
import requests # библиотека для работы с HTTP-запросами

api = (API_KEY)  # создаем экземпляр API
bot = Bot(token=TOKEN) # создаем экземпляр бота
dp = Dispatcher(bot) # создаем экземпляр диспетчера


async def get_cat_image(): # асинхронная функция для получения картинки котика
    url = f"https://api.pexels.com/v1/search?query=cat&per_page=80" # формируем URL запроса с параметрами (изменено)
    headers = {"Authorization": API_KEY} # формируем заголовки запроса с API-ключом
    response = requests.get(url, headers=headers) # отправляем GET-запрос и получаем ответ
    data = response.json() # преобразуем ответ в JSON формат
    image_url = random.choice(data["photos"])["src"]["original"] # извлекаем URL картинки из случайного элемента списка photos (изменено)
    return image_url # возвращаем URL картинки


@dp.message_handler(commands=["cat"]) # обработчик команды /cat (исправлено)
async def send_cat_image(message: types.Message): # асинхронная функция для отправки картинки пользователю
    image_url = await get_cat_image() # вызываем функцию для получения картинки котика
    await bot.send_photo(message.chat.id, image_url) # отправляем картинку пользователю с клавиатурой


@dp.callback_query_handler(lambda query: query.data == "refresh") # обработчик коллбэк-запросов с данными "refresh"
async def refresh_cat_image(query: types.CallbackQuery): # асинхронная функция для обновления картинки котика
    image_url = await get_cat_image() # вызываем функцию для получения новой картинки котика
    await bot.edit_message_media(types.InputMediaPhoto(image_url), query.message.chat.id, query.message.message_id)

executor.start_polling(dp)
