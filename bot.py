from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
import stripe

# --- 1. Токен бота ---
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. Закрытый канал и Stripe ---
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")      # тестовый ключ Stripe

# --- 3. Приветствие ---
@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
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

# --- 4. Меню выбора ---
@dp.message()
async def menu(message: types.Message):
    if message.text == "💄 Курсы":
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="💳 Купить курс за 49€", callback_data="buy")]
            ]
        )
        await message.answer(
            "Курс 'Сам себе визажист'\n💄 Что получишь:\n"
            "- Полный видео-курс\n"
            "- Пошаговые уроки\n"
            "- Советы и секреты профессионалов\n\n"
            "Цена: 49€",
            reply_markup=kb
        )
    elif message.text == "💡 Советы":
        await message.answer(
            "Вот несколько бесплатных лайфхаков для макияжа:\n"
            "- Используй праймер перед тональным кремом\n"
            "- Подводка должна быть тонкой и аккуратной\n"
            "- Смешивай текстуры для естественного эффекта\n\n"
            "Чтобы получить полный курс, нажми '💄 Курсы'"
        )

# --- 5. Кнопка "Купить" + Stripe Test Checkout ---
@dp.callback_query(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    # создаём тестовую сессию Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': 'Курс визажиста'},
                'unit_amount': 4900,  # 49€ в центах
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"https://t.me/{os.getenv('BOT_USERNAME')}?start=paid",
        cancel_url=f"https://t.me/{os.getenv('BOT_USERNAME')}",
        metadata={'telegram_id': callback.from_user.id}
    )

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="💳 Перейти к оплате",
                url=session.url  # ссылка на Stripe Checkout
            )]
        ]
    )

    await callback.message.answer(
        "Нажми кнопку ниже для оплаты (тестовая карта 💳 4242 4242 4242 4242)",
        reply_markup=kb
    )

# --- 6. После оплаты (по параметру success_url) ---
@dp.message(Command(commands=["paid"]))
async def paid(message: types.Message):
    await message.answer(
        f"Спасибо за оплату! 💄\n\nВот твой доступ к курсу:\n{CHANNEL_LINK}\n\n"
        "Присоединяйся и начинай обучение прямо сейчас!"
    )

# --- 7. Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
