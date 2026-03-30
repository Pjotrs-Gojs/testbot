from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 👉 ВСТАВЬ СЮДА СВОЮ ССЫЛКУ НА ЗАКРЫТЫЙ КАНАЛ
CHANNEL_LINK = "https://t.me/+cF63Lh2gxBRmNGNk"

# /start
@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="💄 Курсы")]],
        resize_keyboard=True
    )
    await message.answer("Привет! 💄\nВыбери раздел:", reply_markup=kb)

# меню
@dp.message()
async def menu(message: types.Message):
    if message.text == "💄 Курсы":
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="💳 Купить курс за 49€",
                    callback_data="buy"
                )]
            ]
        )

        await message.answer(
            "Курс 'Сам себе визажист'\nЦена: 49€",
            reply_markup=kb
        )

# кнопка купить
@dp.callback_query(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="💳 Перейти к оплате",
                url="https://t.me/your_username"  # временно можно просто ТГ
            )],
            [types.InlineKeyboardButton(
                text="✅ Я оплатил",
                callback_data="paid"
            )]
        ]
    )

    await callback.message.answer(
        "Нажми кнопку ниже для оплаты 👇",
        reply_markup=kb
    )

# после "я оплатил"
@dp.callback_query(lambda c: c.data == "paid")
async def paid(callback: types.CallbackQuery):
    await callback.message.answer(
        f"Спасибо за оплату! 💄\n\nВот доступ к курсу:\n{CHANNEL_LINK}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
