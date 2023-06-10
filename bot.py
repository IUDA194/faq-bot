import asyncio
import os
import sqlite3 as sql
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.message import ContentType

from config import TOKEN, ADMINS_LIST
from db import database

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
DataBase = database()

# Клавиатурка админа

class insert_q(StatesGroup):
    question = State()
    ansver = State()

admin_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Додати питання", callback_data="insert_q"))

@dp.message_handler(commands=['admin'])
async def start_command(message : types.Message):
    if str(message.from_user.id) in ADMINS_LIST: await bot.send_message(message.from_user.id, "Добрий вечір!", reply_markup=admin_kb)
    else: await message.delete()

@dp.callback_query_handler(text="insert_q")
async def checkAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введіть питання:")
    await insert_q.question.set()

@dp.message_handler(state=insert_q.question)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question'] = message.text
        await bot.send_message(message.from_user.id, "Введіть відповідь на питання:")
        await insert_q.ansver.set()
    else: 
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)

@dp.message_handler(state=insert_q.ansver)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['ansver'] = message.text
            DataBase.insert_new_question(data['question'], data['ansver'])
            await bot.send_message(message.from_user.id, f"Готово, питання {data['question']} додано з відповіддю {data['ansver']}", reply_markup=admin_kb)
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)


@dp.message_handler(commands=['start'])
async def start_command(message : types.Message):
    kb = InlineKeyboardMarkup()

    questions = DataBase.select_all_question()["question"]

    for question in questions:
        kb.add(InlineKeyboardButton(f"{question[0]}", callback_data=f"{question[0]}"))

    await message.delete()
    await bot.send_message(message.from_user.id, """<b>Головне меню!</b>
    
Виберіть своє питання нижче:""", reply_markup=kb)


@dp.callback_query_handler()
async def checkAnswer(callback_query: types.CallbackQuery):
    result = DataBase.select_ansv_from_question(callback_query.data)

    if result["status"]: await bot.send_message(callback_query.from_user.id, result["ansv"])
    else: pass

#запуск бота
async def on_startup(_):
    print('bot online')

executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота
