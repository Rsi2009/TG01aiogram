from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url='https://dzen.ru/news/')],
    [InlineKeyboardButton(text="Аудио", url='https://zvuk.com/track/138000988')],
    [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')],
    [InlineKeyboardButton(text="Картинка", url='https://koshka.top/uploads/posts/2021-12/1639308312_9-koshka-top-p-melkie-koshki-9.jpg')]
    ])


inline_keyboard_test2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='show_more')]
])

inline_keyboard_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новость 1", callback_data='option_1')],
    [InlineKeyboardButton(text="Новость 2", callback_data='option_2')]
])


test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]
async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup()