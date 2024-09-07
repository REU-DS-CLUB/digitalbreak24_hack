from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, keyboard_button
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_inline_start():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Ввести запрос в свободной форме', callback_data="text")
    keyboard_builder.button(text='Ввести запрос в форме голосового сообщения', callback_data="voice")
    keyboard_builder.button(text='Получить предсказание на завтра', callback_data="predict")

    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()