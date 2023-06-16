import asyncio
import os
import re
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

class edit_q(StatesGroup):
    question = State()
    question_new = State()

class edit_q_t(StatesGroup):
    question = State()
    question_new = State()

class delate_q(StatesGroup):
    question = State()

admin_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Додати питання", callback_data="insert_q"),
                                                InlineKeyboardButton("Змінити питання заголовок", callback_data="edit_q"),
                                                InlineKeyboardButton("Змінити питання текст", callback_data="edit_q_t"),
                                                InlineKeyboardButton("Видалити питання", callback_data="delate_q"))

to_menu_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Повернутися до списку питань", callback_data="back_to_main"))

@dp.message_handler(commands=['admin'])
async def start_command(message : types.Message):
    if str(message.from_user.id) in ADMINS_LIST: await bot.send_message(message.from_user.id, "Добрий вечір!", reply_markup=admin_kb)
    else: await message.delete()



@dp.callback_query_handler(text="back_to_main")
async def checkAnswer(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup()

    questions = DataBase.select_all_question()["question"]

    for question in questions:
        kb.add(InlineKeyboardButton(f"{question[0]}", callback_data=re.sub('[^\x00-\x7Fа-яА-Я]', '', f"{question[0]}"[:30])))
    kb.add(InlineKeyboardButton("Не знайшли відповідь на своє питання", callback_data="no_ansv"))

    #await callback_query.message.delete()
    await bot.send_message(callback_query.message.chat.id, """<b>Головне меню!</b>
    
Виберіть своє питання нижче:""", reply_markup=kb)
    



@dp.callback_query_handler(text="insert_q")
async def checkAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введіть питання:")
    await insert_q.question.set()

@dp.callback_query_handler(text="delate_q")
async def checkAnswer(callback_query: types.CallbackQuery):

    kb = ReplyKeyboardMarkup()

    questions = DataBase.select_all_question()["question"]

    for question in questions:
        kb.add(KeyboardButton(re.sub('[^\x00-\x7Fа-яА-Я]', '', f"{question[0]}")))

    await bot.send_message(callback_query.from_user.id, "Введіть питання:", reply_markup=kb)
    await delate_q.question.set()

@dp.callback_query_handler(text="edit_q")
async def checkAnswer(callback_query: types.CallbackQuery):

    kb = ReplyKeyboardMarkup()

    questions = DataBase.select_all_question()["question"]

    for question in questions:
        kb.add(KeyboardButton(re.sub('[^\x00-\x7Fа-яА-Я]', '', f"{question[0]}")))

    await bot.send_message(callback_query.from_user.id, "Введіть питання:", reply_markup=kb)
    await edit_q.question.set()

@dp.message_handler(state=delate_q.question)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question'] = message.text
            DataBase.delate_question(data['question'])
            await bot.send_message(message.from_user.id, f"Готово", reply_markup=admin_kb)
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)


@dp.message_handler(state=edit_q.question)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question'] = message.text
            await bot.send_message(message.from_user.id, f"Готово, введіть змінене питання:")
        await edit_q.question_new.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)

@dp.message_handler(state=edit_q.question_new)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question_new'] = message.text
            DataBase.edit_question_hedder(data['question'], data['question_new'])
            await bot.send_message(message.from_user.id, f"Готово")
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)


@dp.callback_query_handler(text="edit_q_t")
async def checkAnswer(callback_query: types.CallbackQuery):

    kb = ReplyKeyboardMarkup()

    questions = DataBase.select_all_question()["question"]

    for question in questions:
        kb.add(KeyboardButton(re.sub('[^\x00-\x7Fа-яА-Я]', '', f"{question[0]}")))

    await bot.send_message(callback_query.from_user.id, "Введіть питання:", reply_markup=kb)
    await edit_q_t.question.set()

@dp.message_handler(state=edit_q_t.question)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question'] = message.text
            await bot.send_message(message.from_user.id, f"Готово, введіть змінене питання:")
        await edit_q_t.question_new.set()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)

@dp.message_handler(state=edit_q_t.question_new)
async def start_command(message : types.Message, state: FSMContext):
    if message.text.upper() != "НАЗАД":
        async with state.proxy() as data:
            data['question_new'] = message.text
            DataBase.edit_question_ansv(data['question'], data['question_new'])
            await bot.send_message(message.from_user.id, f"Готово")
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=admin_kb)

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
        kb.add(InlineKeyboardButton(f"{question[0]}", callback_data=re.sub('[^\x00-\x7Fа-яА-Я]', '', f"{question[0]}"[:30])))
    kb.add(InlineKeyboardButton("Не знайшли відповідь на своє питання", callback_data="no_ansv"))

    await message.delete()
    await bot.send_message(message.from_user.id, """<b>Головне меню!</b>
    
Виберіть своє питання нижче:""", reply_markup=kb)

@dp.callback_query_handler(text='no_ansv')
async def checkAnswer(callback_query: types.CallbackQuery):
    await callback_query.answer("Напищіть на почту коледжу: kpcc@meta.ua", show_alert=True)

@dp.callback_query_handler()
async def checkAnswer(callback_query: types.CallbackQuery):
    result = DataBase.select_ansv_from_question(callback_query.data)

    if result["status"]: await bot.send_message(callback_query.from_user.id, result["ansv"], reply_markup=to_menu_kb)
    else: pass

@dp.message_handler()
async def start_command(message : types.Message):
    await bot.send_message(message.from_user.id, "<b>Добрий вечір!</b>", reply_markup=to_menu_kb)
#запуск бота
async def on_startup(_):
    print('bot online')

executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота
