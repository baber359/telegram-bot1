import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = "8663120102:AAFKahmAp2fLdPwwJtkmUh3MBmlVaJSCZFw"
ADMIN_ID = 6021257033

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 🚀 Меню:\n"
        "1 - Заказать сборку\n"
        "2 - Предложить идеи для сборки\n"
        "3 - Идеи для улучшения бота\n"
        "4 - Жалобы"
    )

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "1":
        await message.answer("Напишите, что хотите в вашей сборке.\nЕсли есть фото — прикрепите.")
    elif message.text == "2":
        await message.answer("Напишите идею, которую хотите предложить.")
    elif message.text == "3":
        await message.answer("Напишите, что можно улучшить в боте.")
    elif message.text == "4":
        await message.answer("Напишите вашу жалобу.")
    else:
        await bot.send_message(ADMIN_ID, f"Сообщение от @{message.from_user.username}:\n{message.text}")
        await message.answer("Ваше сообщение отправлено администратору ✅")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
