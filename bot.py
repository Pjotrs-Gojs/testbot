from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio
import os
import stripe

# --- ENV ---
TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")  # без @
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# --- INIT ---
bot = Bot(token=TOKEN)
dp = Dispatcher()
stripe.api_key = STRIPE_SECRET_KEY

# --- START ---
@dp.message(CommandStart())
async def start(message: types.Message):
    args = message.text.split()

    # если пришёл после оплаты
    if len(args) > 1 and args[1] == "paid":
        await message.answer(
            f"Спасибо за оплату! 💄\n\n"
            f"Вот твой доступ к курсу:\n{CHANNEL_LINK}\n\n"
            f"Присоединяйся и начинай обучение!"
        )
        return

    # обычный старт
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="💄 Курсы")],
            [types.KeyboardButton(text="💡 Советы")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Привет! 💄\nЯ помогу тебе стать экспертом в визажe!\n\nВыбери раздел:",
        reply_markup=kb
    )

# --- MENU ---
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
            "Курс 'Сам себе визажист'\n\n"
            "💄 Что ты получишь:\n"
            "- Полный видео-курс\n"
            "- Пошаговые уроки\n"
            "- Секреты визажистов\n\n"
            "💰 Цена: 49€",
            reply_markup=kb
        )

    elif message.text == "💡 Советы":
        await message.answer(
            "💡 Бесплатные советы:\n\n"
            "— Используй праймер\n"
            "— Лёгкая растушёвка = натуральный вид\n"
            "— Не перегружай тон\n\n"
            "Хочешь полный курс? Нажми 💄 Курсы"
        )

# --- BUY ---
@dp.callback_query(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Курс визажиста',
                    },
                    'unit_amount': 4900,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"https://t.me/{BOT_USERNAME}?start=paid",
            cancel_url=f"https://t.me/{BOT_USERNAME}",
            metadata={
                "telegram_id": callback.from_user.id
            }
        )

        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="💳 Перейти к оплате",
                    url=session.url
                )]
            ]
        )

        await callback.message.answer(
            "Нажми кнопку ниже для оплаты 👇\n\n"
            "💳 Тестовая карта:\n"
            "4242 4242 4242 4242\n"
            "Любая дата и CVC",
            reply_markup=kb
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка при создании оплаты: {e}")

# --- RUN ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
