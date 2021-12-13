from aiogram import Bot, Dispatcher, executor, types, asyncio

import os
import glob
from datetime import datetime
import time
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config.get('DEFAULT', 'API_TOKEN')
CHAT_ID = config["DEFAULT"]["CHAT_ID"]
PATH = config["DEFAULT"]["PATH"]

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
x=11

async def add_photo(time):
    filename_list = glob.glob(PATH)
    filename = filename_list[0]
    photo = open(filename, 'rb')
    logging.info('Пост опубликован')
    await bot.send_photo(CHAT_ID, photo)
    photo.close()
    os.remove(filename)

async def add_gif(time):
    filename_list = glob.glob(PATH)
    filename = filename_list[0]
    photo = open(filename, 'rb')
    logging.info('Пост опубликован')
    await bot.send_animation(CHAT_ID, photo, caption=time)
    photo.close()
    os.remove(filename)
    
async def start_post(x):
    print('Цикл начался')
    logging.info('Цикл начался')
    while True:
        time = datetime.now()
        if time.hour==7 and x==0:
            x=7
            await asyncio.create_task(add_photo(time))
        elif time.hour==9 and x==7:
            x=9
            await asyncio.create_task(add_photo(time))
        elif time.hour==11 and x==9:
            x=11
            await asyncio.create_task(add_photo(time))
        elif time.hour==15 and x==11:
            x=15
            await asyncio.create_task(add_photo(time))
        elif time.hour==17 and x==15:
            x=17
            await asyncio.create_task(add_photo(time))
        elif time.hour==19 and x==17:
            x=19
            await asyncio.create_task(add_photo(time))
        elif time.hour==21 and x==19:
            x=21
            await asyncio.create_task(add_photo(time))
        elif time.hour==23 and x==21:
            x=0
            await asyncio.create_task(add_photo(time))
        await asyncio.sleep(1200) #Работает! Можно попасть в бесконечный цикл
        
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    asyncio.create_task(start_post(x))
    print('Начало постинга')
    logging.info('Постинг начался')
    await message.reply(f'Добро пожаловать {message.from_user.first_name}. Бот активирован')

@dp.message_handler(commands=['status'])
async def send_status(message: types.Message):
    logging.info(message)
    await message.reply(f'Я всё еще жив! {datetime.now().hour}')

@dp.message_handler(commands=['test'])
async def send_test(message: types.Message):
    logging.info(message)
    await asyncio.create_task(add_gif(datetime.now()))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
