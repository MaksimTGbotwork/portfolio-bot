from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from handleres.keyboard import inline_kb as kb
from handleres.keyboard import payment_kb as markup

pay = Router()


@pay.message(Command("pay"))
async def str_pay(message: Message):
    await message.answer("Здравствуйте! Выберите подходящий тариф:", reply_markup=kb)


@pay.message(Command("back"))
async def back(message: Message, bot: Bot, command: CommandObject):
    await bot.refund_star_payment(
        user_id=message.from_user.id, telegram_payment_charge_id=command.args
    )


@pay.callback_query(F.data == "subscribe")
async def handle_subscribe(call: CallbackQuery):
    price = [LabeledPrice(label="XTR", amount=1)]
    await call.message.answer_invoice(
        title="Подписка на бота",
        description="Уровень Админ. Которая позволяет смотреть транзакции",
        prices=price,
        provider_token="",
        payload="by stars",
        currency="XTR",
        reply_markup=markup,
    )


@pay.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@pay.message(F.successful_payment)
async def success_payment(message: Message):
    await message.answer(f"{message.successful_payment.telegram_payment_charge_id}")
    await message.answer("<b>Спасибо за оплату!</b>", parse_mode="HTML")
