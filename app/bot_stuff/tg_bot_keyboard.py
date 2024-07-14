from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                            InlineKeyboardButton, InlineKeyboardMarkup)


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Перезапустить бота'),
    KeyboardButton(text='Скачать документы')]
    ],
    resize_keyboard=True)