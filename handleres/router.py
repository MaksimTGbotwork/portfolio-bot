

import aiosqlite
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from forms.user import Form
from handleres.keyboard import inline as inl
from handleres.keyboard import inline_kb as kb
from handleres.keyboard import menu as kd
from handleres.keyboard import payment_kb as markup

router = Router()


@router.message(Command("pay"))
async def str_pay(message: Message):
    await message.answer("Привет! Давай протестируем оплаты", reply_markup=kb)

@router.message(Command('back'))
async def back(message: Message, bot: Bot, command: CommandObject):
    await bot.refund_star_payment(user_id=message.from_user.id, telegram_payment_charge_id=command.args)

@router.callback_query(F.data == "subscribe")
async def handle_subscribe(call: CallbackQuery):
    price = [LabeledPrice(label='XTR', amount=1)]
    await call.message.answer_invoice(
        title='Подписка на бота',
        description='Возможность пользоваться ботом',
        prices=price,
        provider_token= "",
        payload="by stars",
        currency='XTR',
        reply_markup=markup
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def success_payment(message: Message):
    await message.answer(f'{message.successful_payment.telegram_payment_charge_id}')
    await message.answer('<b>Спасибо за оплату!</b>', parse_mode='HTML')
# -- --

DB_NAME = "swuike.sql"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            age INTEGER
            )
                         """)
        await db.commit()


async def add_users(full_name, age):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (full_name, age) VALUES(?, ?)", (full_name, age)
        )
        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
        return result


@router.message(Command("weg"))
async def weg(message: Message):
    await init_db()
    await message.answer("Привет!\nПропишите команду: /weg AGE")


@router.message(Command("reg"))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Введите команду верно!")
        return

    await add_users(message.from_user.full_name, int(parts[1]))

    await message.answer("Все готово!")


@router.message(Command("users"))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer("В базе нет пользователей")
        return

    text = "Пользователи в базе:\n\n"
    for full_name, age in users:
        text += f"- {full_name} - <code>{age}</code>\n"

    await message.answer(text, parse_mode="HTML")


# -- --


@router.callback_query(lambda c: c.data == "info_more")
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer("Вот подробная информация")
    await callback.answer()


@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def hello(message: Message):
    await message.answer(
        "Привет! Я *простой* бот _для_ тебя\n\n Напиши /help для помощи",
        parse_mode="Markdown",
        reply_markup=inl,
    )


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Команды: \n<b>/start</b> - Запустить бот\n<i>/help</i> - Список <a href ='https://google.com'> команд</a>\n/about - про нас",
        parse_mode="HTML",
        reply_markup=kd,
    )


@router.message(Command("about"))
async def about(message: Message):
    await message.answer(
        f"Это команда про бота. Твое имя: {message.from_user.first_name}"
    )


@router.message(Command("User"))
async def user(message: Message, state: FSMContext):
    await message.answer("Давайте начнем заполнять анкету!\nСперва введите ваше имя:")
    await state.set_state(Form.name)


@router.message(Command("cancel"))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отклонена!")


@router.message(Form.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Отлично!\nА теперь введите ваш возраст:")
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должным быть числом")
        return

    if int(message.text) < 1 or int(message.text) > 100:
        await message.answer("Возраст должен быть  от 1 до 100")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Отлично!\nА теперь введите ваш email:")
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
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

    await message.answer(f"Анкета готова!\nИмя: {name}\nВозраст: {age}\nПочта: {email}")
    await state.clear()


@router.message(F.photo)
async def proccess_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(
        f"Вы отправили фото!\nID photo: <code>{file_id}</code>", parse_mode="HTML"
    )

    await message.answer_photo(file_id, caption="Вот ваше фото!")


@router.message(F.video)
async def proccess_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(
        f"Вы отправили видео!\nID video: <code>{file_id}</code>\nДлительность: <code>{duration}</code>",
        parse_mode="HTML",
    )

    await message.answer_video(file_id, caption="Вот ваше видео!")


@router.message(F.animation)
async def proccess_animation(message: Message):
    animation = message.animation

    await message.answer(
        f"Вы отправили animation!\nID animation: <code>{animation.file_id}</code>",
        parse_mode="HTML",
    )

    await message.answer_animation(animation.file_id, caption="Вот ваше animation!")


@router.message(F.document)
async def proccess_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f"downloads/{document.file_name}"

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer("Файл сохранен!")


@router.message(Command("file"))
async def send_file(message: Message):
    file = FSInputFile("files/example.txt")

    await message.answer_document(file)


@router.message()
async def mess(message: Message):
    await message.answer("Text message")
