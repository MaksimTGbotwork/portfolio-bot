from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О боте", style="primary")],
        [
            KeyboardButton(text="Старт", style="success"),
            KeyboardButton(text="Помощь", style="danger"),
        ],
    ],
    resize_keyboard=True,
)


inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть сайт", style="primary", url="https://google.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Подробнее", style="success", callback_data="info_more"
            )
        ],
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
    inline_keyboard=[[InlineKeyboardButton(text="Оплатить🌟", pay=True)]]
)
