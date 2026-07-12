import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

TOKEN = "8663120102:AAFKahmAp2fLdPwwJtkmUh3MBmlVaJSCZFw"
ADMIN_ID = 6021257033

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_states = {}

# 🔥 Красивое меню
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Заказать сборку", callback_data="order")],
        [InlineKeyboardButton(text="❗ Жалоба", callback_data="complaint")]
    ])
    return kb

def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🔥 Добро пожаловать!\n\nВыберите действие:", reply_markup=main_menu())

# Обработка кнопок
@dp.callback_query()
async def callbacks(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "order":
        user_states[user_id] = "order"
        await callback.message.edit_text(
            "📦 Напишите что хотите в вашей сборке\n\nМожно отправить текст + фото",
            reply_markup=back_button()
        )

    elif callback.data == "complaint":
        user_states[user_id] = "complaint"
        await callback.message.edit_text(
            "❗ Напишите вашу жалобу",
            reply_markup=back_button()
        )

    elif callback.data == "back":
        user_states[user_id] = None
        await callback.message.edit_text(
            "🔥 Главное меню:",
            reply_markup=main_menu()
        )

# 📩 Обработка сообщений
@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if state == "order":
        text = message.caption or message.text or "Без текста"

        # Отправка админу
        if message.photo:
            msg = await bot.send_photo(
                ADMIN_ID,
                photo=message.photo[-1].file_id,
                caption=f"📦 ЗАКАЗ\nОт: {user_id}\n\n{text}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user_id}")]
                ])
            )
        else:
            msg = await bot.send_message(
                ADMIN_ID,
                f"📦 ЗАКАЗ\nОт: {user_id}\n\n{text}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user_id}")]
                ])
            )

        await message.answer("✅ Заказ отправлен! Ожидайте ответа.")
        user_states[user_id] = None

    elif state == "complaint":
        text = message.caption or message.text or "Без текста"

        if message.photo:
            await bot.send_photo(
                ADMIN_ID,
                photo=message.photo[-1].file_id,
                caption=f"❗ ЖАЛОБА\nОт: {user_id}\n\n{text}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user_id}")]
                ])
            )
        else:
            await bot.send_message(
                ADMIN_ID,
                f"❗ ЖАЛОБА\nОт: {user_id}\n\n{text}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user_id}")]
                ])
            )

        await message.answer("✅ Жалоба отправлена!")
        user_states[user_id] = None

# 🔥 Ответ админа кнопкой
@dp.callback_query(lambda c: c.data.startswith("reply_"))
async def reply_start(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    user_states[callback.from_user.id] = f"reply_{user_id}"

    await callback.message.answer("✍️ Напиши ответ пользователю:")

# Отправка ответа
@dp.message()
async def admin_reply(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        state = user_states.get(ADMIN_ID)

        if state and state.startswith("reply_"):
            user_id = int(state.split("_")[1])

            await bot.send_message(user_id, f"📩 Ответ от владельца:\n\n{message.text}")
            await message.answer("✅ Ответ отправлен!")

            user_states[ADMIN_ID] = None

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
