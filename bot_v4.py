from aiogram import Bot, Dispatcher, types, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters import Command
from aiogram.types import FSInputFile
from functions.posts import posts_list, add_posts

import asyncio
import concurrent.futures

import os
import glob
from datetime import datetime
import logging
import configparser
import random

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

API_TOKEN = config["DEFAULT"]["API_TOKEN"]

FAKEHUB_ID = config["HUB"]["CHAT_ID"]
FAKEHUB_PATH = config["HUB"]["PATH"]
FAKEHUB_VIDEO = config["HUB"]["VIDEO"]

NINJAS_ID = config["NINJA"]["CHAT_ID"] 
NINJAS_PATH = config["NINJA"]["PATH"]

SILENTGIRL_ID = config["GIRL"]["CHAT_ID"]
SILENTGIRL_PATH = config["GIRL"]["PATH"]

TEST_ID = config["TEST"]["CHAT_ID"]
TEST_PATH = config["TEST"]["PATH"]

session = AiohttpSession(
    api=TelegramAPIServer.from_base('http://localhost:8081')
)
bot = Bot(token=API_TOKEN,session=session)
dp = Dispatcher()
x=0

async def add_photo(channel, path):
    try:
        filename_list = glob.glob(path)
        filename = filename_list[0]
        file = FSInputFile(filename)
    except Exception:
        logging.info(f'Директория пуста: {path}')
        print(f'Директория пуста: {path}')
    else:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            await bot.send_photo(channel, file) 
        elif filename.lower().endswith(('.gif', '.mp4')):
            await bot.send_animation(channel, file)
        logging.info('Пост опубликован')
        os.remove(filename)

async def add_video(channel, path):
    try:
        filename_list = glob.glob(path)
        filename = random.choice(filename_list)
        file = FSInputFile(filename)

        file_caption = os.path.splitext(os.path.basename(filename))[0]
        caption = f"{file_caption}" "\n" "#video"

    except Exception as e:
        logging.info(f'Директория пуста: {path}')
        print(f'Директория пуста: {path}')
    else:
        await bot.send_video(channel, file, caption=caption, request_timeout=10000)
        logging.info(f'Видео опубликовано: {path}')
        #os.remove(filename)

async def start_post(x):
    while True:
        time = datetime.now().hour
        if time==6 and x==6:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==7 and x==7:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==8 and x==8:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==9 and x==9:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==10 and x==10:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==11 and x==11:
            x=13
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==13 and x==13:
            x+=1
            await asyncio.create_task(add_video(FAKEHUB_ID, FAKEHUB_VIDEO))
        elif time==14 and x==14:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==15 and x==15:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==16 and x==16:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==17 and x==17:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==18 and x==18:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==19 and x==19:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==20 and x==20:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==21 and x==21:
            x+=1
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        elif time==22 and x==22:
            x+=1
            await asyncio.create_task(add_photo(NINJAS_ID, NINJAS_PATH))
            await asyncio.create_task(add_photo(SILENTGIRL_ID, SILENTGIRL_PATH))
        elif time==23 and x==23:
            x=6
            await asyncio.create_task(add_photo(FAKEHUB_ID, FAKEHUB_PATH))
        await asyncio.sleep(1200) #Работает! Можно попасть в бесконечный цикл
        
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    if 23 < datetime.now().hour < 6:
        x = 6
    else: x = datetime.now().hour
    asyncio.create_task(start_post(x))
    print('Начало постинга')
    logging.info('Постинг начался')
    await message.reply(f'Добро пожаловать {message.from_user.first_name}. Бот активирован')

@dp.message(Command(commands=['status']))
async def send_status(message: types.Message):
    file = FSInputFile('app.log')
    await message.reply_document(file)

@dp.message(Command(commands=['video']))
async def send_video(message: types.Message):
    await asyncio.create_task(add_video(TEST_ID, TEST_PATH))
    await message.reply(f'Видео отправлено')

async def main():
    bot = Bot(token=API_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
