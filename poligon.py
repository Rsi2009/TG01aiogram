import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN, POLIGON_API_KEY


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command('start'))
async def start(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}!\n"
                         f"Добро пожаловать в наш бот для получения котировок акций!\n"
                         f"Спасибо за использование нашего сервиса. Введите символ акции (например, AAPL для Apple), чтобы получить последнюю котировку.")
@dp.message(Command('quote'))
async def get_stock_quote(message: Message):
    await message.answer("Введите символ акции, чтобы получить последнюю котировку (например, AAPL для Apple):")

    @dp.message()
    async def handle_stock_symbol(message: Message):
        symbol = message.text.upper()
        url = f'https://api.polygon.io/v1/last/stocks/{symbol}?apiKey={POLIGON_API_KEY}'

        try:
            response = requests.get(url)
            data = response.json()

            # Логирование полного ответа от API для отладки
            logging.info(f"API response: {data}")

            # Проверка наличия поля 'last' в ответе
            if 'last' in data:
                price = data['last']['price']
                await message.answer(f"Последняя цена акции {symbol}: ${price}")
            else:
                await message.answer("Произошла ошибка: данные о цене не найдены.")

        except Exception as e:
            logging.error(f"Ошибка при получении данных: {e}")
            await message.answer(f"Произошла ошибка при получении данных: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())


