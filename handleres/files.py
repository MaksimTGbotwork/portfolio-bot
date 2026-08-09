from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    FSInputFile,
    Message,
)

file = Router()


@file.message(F.photo)
async def proccess_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    await message.answer(
        f"Вы отправили фото!\nID photo: <code>{file_id}</code>", parse_mode="HTML"
    )
    await message.answer_photo(file_id, caption="Вот ваше фото!")


@file.message(F.video)
async def proccess_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration
    await message.answer(
        f"Вы отправили видео!\nID video: <code>{file_id}</code>\nДлительность: <code>{duration}</code>",
        parse_mode="HTML",
    )
    await message.answer_video(file_id, caption="Вот ваше видео!")


@file.message(F.animation)
async def proccess_animation(message: Message):
    animation = message.animation
    await message.answer(
        f"Вы отправили animation!\nID animation: <code>{animation.file_id}</code>",
        parse_mode="HTML",
    )
    await message.answer_animation(animation.file_id, caption="Вот ваше animation!")


@file.message(F.document)
async def proccess_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    local_path = f"downloads/{document.file_name}"
    await bot.download_file(file_path=file_path, destination=local_path)
    await message.answer("Файл сохранен!")


@file.message(Command("file"))
async def send_file(message: Message):
    file = FSInputFile("files/example.txt")
    await message.answer_document(file)
