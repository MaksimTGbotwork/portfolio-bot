from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

comm = Router()

from handleres.keyboard import inline as inl
from handleres.keyboard import menu as kd


@comm.message(Command("start"))
@comm.message(F.text.lower() == "старт")
async def hello(message: Message):
    await message.answer(
        "Привет! Я *простой* бот _для_ тебя\n\n Напиши /help для помощи",
        parse_mode="Markdown",
        reply_markup=inl,
    )


@comm.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Команды: \n<b>/start</b> - Запустить бот\n<i>/help</i> - Список <a href ='https://google.com'> команд</a>\n/about - про нас",
        parse_mode="HTML",
        reply_markup=kd,
    )


@comm.message(Command("about"))
async def about(message: Message):
    await message.answer(
        f"Команда /about — показывает информацию о боте и о тебе. Твое имя: {message.from_user.first_name}"
    )


@comm.callback_query(F.data == "info_more")
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer("Вот подробная информация")
    await callback.answer()


@comm.message()
async def mess(message: Message):
    await message.answer("Text message")
