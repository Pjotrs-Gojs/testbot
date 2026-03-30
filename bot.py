from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TOKEN = "8640058416:AAG_WJfXlC7viPzkbtc9o_sZpLu4dc3zO5o"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Правильная регистрация команды /start
@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="💄 Курсы")]],
        resize_keyboard=True
    )
    await message.answer("Привет! 💄\nВыбери раздел:", reply_markup=kb)

@dp.message()
async def menu(message: types.Message):
    if message.text == "💄 Курсы":
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="💳 Купить курс за 49€", callback_data="buy")]
            ]
        )
        await message.answer("Курс 'Сам себе визажист'\nЦена: 49€", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    await callback.message.answer("Скоро тут будет оплата 💳")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
