from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import get_profile, save_profile
from forms.user import Form

registration = Router()


@registration.message(Command("user"))
async def user(message: Message, state: FSMContext):
    await message.answer(
        "Давайте начнем заполнять анкету!\nСперва мне нужно узнать ваше имя:"
    )
    await state.set_state(Form.name)


@registration.message(Command("cancel"))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отклонена!")


@registration.message(Form.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично!\nА теперь мне нужно узнать ваш возраст:")
    await state.set_state(Form.age)


@registration.message(Form.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должным быть числом")
        return

    if int(message.text) < 1 or int(message.text) > 100:
        await message.answer("Возраст должен быть от 1 до 100")
        return

    await state.update_data(age=int(message.text))
    await message.answer("Отлично!\nА теперь введите ваш email:")
    await state.set_state(Form.email)


@registration.message(Form.email, F.text)
async def proccess_email(message: Message, state: FSMContext):
    email_text = message.text
    if "@" not in email_text or "." not in email_text:
        await message.answer("Email не корректный")
        return

    await state.update_data(email=email_text)

    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    email = data["email"]

    await save_profile(message.from_user.id, name, age, email)

    await message.answer(
        f"Анкета готова и сохранена!\nИмя: {name}\nВозраст: {age}\nПочта: {email}"
    )
    await state.clear()


@registration.message(Command("myprofile"))
async def my_profile(message: Message):
    profile = await get_profile(message.from_user.id)

    if profile is None:
        await message.answer(
            "У вас ещё нет заполненной анкеты. Введите /user чтобы заполнить."
        )
        return

    name, age, email = profile
    await message.answer(f"Ваш профиль:\nИмя: {name}\nВозраст: {age}\nПочта: {email}")
