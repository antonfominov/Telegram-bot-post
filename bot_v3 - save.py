from aiogram import Bot, Dispatcher, executor, types, asyncio

import os
import glob
from datetime import datetime
import time
import logging

API_TOKEN = ''
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
x=0

async def add_post(current_datetime):
    filename_list = glob.glob('')
    filename = filename_list[0]
    photo = open(filename, 'rb')
    logging.info('Пост опубликован')
    await bot.send_photo(-1001386365789, photo, caption=current_datetime)
    photo.close()
    os.remove(filename)

async def start_post(x):
    print('Цикл начался')
    while True:
        current_datetime = datetime.now()
        if current_datetime.minute==50 and x==0:
            x=6
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==55 and x==6:
            x=8
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==0 and x==8:
            x=10
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==5 and x==10:
            x=14
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==10 and x==14:
            x=16
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==15 and x==16:
            x=18
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==20 and x==18:
            x=20
            await asyncio.create_task(add_post(current_datetime))
        elif current_datetime.minute==25 and x==20:
            x=22
            await asyncio.create_task(add_post(current_datetime))
        await asyncio.sleep(150) #Работает! Можно попасть в бесконечный цикл
        
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    asyncio.create_task(start_post(x))
    print('Начало постинга')
    await message.reply(f'Добро пожаловать {message.from_user.first_name}. Бот активирован')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
