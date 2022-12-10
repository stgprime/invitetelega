import time
import logging
import asyncio
import sqlite3
import json
#---------------------------------------------------#
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
#---------------------------------------------------#
import keyboard as kb #type: ignore
from config import API_TOKEN, admin, invite, vkgroup
#---------------------------------------------------#
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

connection = sqlite3.connect('data.db')
q = connection.cursor()

q.execute('CREATE TABLE IF NOT EXISTS users (user_id integer)')
connection.commit()

class sender(StatesGroup):
    text = State()

@dp.message_handler(content_types=['text'], text='✉️ Discord Сервер')
async def takeamail(m: types.Message):
    await m.answer(
        '📫 Вот ссылка на Discord:'+invite+'\nJoin Us.\n'
        'Ссылка не меняется, можете её скинуть своему другу!\n\n')
    await asyncio.sleep(5)

@dp.message_handler(content_types=['text'], text='🔐 ВК Группа')
async def takevk(m: types.Message):
    await m.answer(
        '📫 Вот ссылка на нашу группу ВК:'+vkgroup+'\nJoin Us.\n'
        'Ссылка не меняется, можешь скинуть её своему другу!')
    await asyncio.sleep(5)

@dp.message_handler(commands=['admin'])
async def adminstration(m: types.Message):
    if m.chat.id == admin:
        await m.answer('Добро пожаловать в админ панель.', reply_markup=kb.apanel)  #type: ignore
    else:
        await m.answer('Incorrect command.')

@dp.message_handler(content_types=['text'])
async def texthandler(m: types.Message):
    q.execute(f"SELECT * FROM users WHERE user_id = {m.chat.id}")
    result = q.fetchall()
    if len(result) == 0:
        uid = 'user_id'
        sql = 'INSERT INTO users ({}) VALUES ({})'.format(uid, m.chat.id)
        q.execute(sql)
        connection.commit()
    await m.answer(f'Приветствую тебя, {m.from_user.mention}\nЭтот бот создан для быстрого получения инвайта.\nИспользуй кнопки ниже 👇', reply_markup=kb.menu)  # type: ignore

@dp.callback_query_handler(text='stats')
async def statistics(call):
    row = q.execute('SELECT * FROM users').fetchall()
    lenght = len(row)
    await call.message.answer('Всего пользователей: {}'.format(lenght))

@dp.callback_query_handler(text='rass')
async def usender(call):
    await call.message.answer('Введите текст для рассылки.\n\nДля отмены нажмите кнопку ниже 👇', reply_markup=kb.back)  # type: ignore
    await sender.text.set()


@dp.message_handler(state=sender.text)
async def process_name(message: types.Message, state: FSMContext):
    info = q.execute('SELECT user_id FROM users').fetchall()
    if message.text == 'Отмена':
        await message.answer('Отмена! Возвращаю в главное меню.', reply_markup=kb.menu)  # type: ignore
        await state.finish()
    else:
        await message.answer('Начинаю рассылку...', reply_markup=kb.menu)  # type: ignore
        for i in range(len(info)):
            try:
                await bot.send_message(info[i][0], str(message.text))
            except:
                pass
        await message.answer('Рассылка завершена.')
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запуск


