from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О боте")],
        [KeyboardButton(text="Старт"), KeyboardButton(text="Помощь")],
    ],
    resize_keyboard=True,
)


inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Открыть сайт", url="https://google.com")],
        [InlineKeyboardButton(text="Подробнее", callback_data="info_more")],
    ],
    resize_keyboard=True,
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить подписку🌟", callback_data="subscribe")],
    ],
    resize_keyboard=True,

)

payment_kb = InlineKeyboardMarkup(
    inline_keyboard =[
        [InlineKeyboardButton(text="Оплатить🌟", pay=True)]
    ]
)
