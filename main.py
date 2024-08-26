import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
from googletrans import Translator
import asyncio

import random

from gtts import gTTS
import os


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_weather(city: str) -> str:
    # URL для запроса к OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_description = data["weather"][0]["description"]
                    temperature = data["main"]["temp"]
                    return f"В городе {city} сейчас {weather_description}, температура {temperature}°C."
                elif response.status == 404:
                    return "Город не найден. Проверьте название и попробуйте снова."
                else:
                    return f"Ошибка при получении данных: {response.status}"
    except aiohttp.ClientError as e:
        return f"Ошибка сети: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"

@dp.message(Command('weather'))
async def weather(message: Message):
    try:
        # Получение названия города от команды пользователя
        city = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        if not city:
            await message.answer("Пожалуйста, укажите город после команды /weather.")
        else:
            weather_report = await get_weather(city)
            await message.answer(weather_report)
    except Exception as e:
        # Отправляем сообщение с более подробной ошибкой
        await message.answer(f"Произошла ошибка при получении прогноза погоды: {str(e)}")


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("Doc.pdf")
    await bot.send_document(message.chat.id, doc)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile('training.ogg')
   await bot.send_voice(chat_id=message.chat.id, voice=audio)
   os.remove("training.mp3")


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://koshka.top/uploads/posts/2021-12/1639308312_9-koshka-top-p-melkie-koshki-9.jpg',
            'https://kartinki.pics/uploads/posts/2022-12/1670023716_kartinkin-net-p-koshki-malenkie-milie-vkontakte-51.jpg',
            'https://w-dog.ru/wallpapers/3/13/332462222211471/malenkij-slepoj-kotenok-na-ruke.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather <город>")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветики, {message.from_user. first_name}!")


translator = Translator()
@dp.message()
async def translate_message(message: Message):
    translated = translator.translate(message.text, dest='en')
    await message.answer(translated.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
