import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN, WEATHER_API_KEY
from googletrans import Translator
import asyncio

import random

from gtts import gTTS
import os

import keyboards as kb


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main)

@dp.message(F.text == "Привет")
async def test_button(message: Message):
   await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.main)

@dp.message(F.text == "Пока")
async def test_button(message: Message):
   await message.answer(f'До свидания, {message.from_user.first_name}', reply_markup=kb.main)


@dp.message(Command('links'))
async def links(message: Message):
   await message.answer(f'Выбирай кнопку, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)


@dp.message(Command('dinamic'))
async def dinamic(message: Message):
   await message.answer(f'Выбирай новость, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test2)

@dp.callback_query(F.data =='show_more')
async def show_more(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=kb.inline_keyboard_options)

@dp.callback_query(F.data =='option_1')
async def option_1(callback: CallbackQuery):
    await callback.message.answer('Вы выбрали Новость 1')

@dp.callback_query(F.data =='option_2')
async def option_1(callback: CallbackQuery):
    await callback.message.answer('Вы выбрали Новость 2')


@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
   await callback.answer("Новости подгружаются", show_alert=True)
   await callback.message.answer('Вот свежие новости!')







@dp.message(Command('new'))
async def new(message: Message):
   await message.answer(f'Выбирай, {message.from_user.first_name}', reply_markup=await kb.test_keyboard())



async def main():
   await dp.start_polling(bot)


if __name__ == "__main__":
   asyncio.run(main())