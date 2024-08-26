import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY
import random

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

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather <город>")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
