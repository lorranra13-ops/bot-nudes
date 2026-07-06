import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1004260845425  # Vamos pegar automaticamente

bot = Bot(token=TOKEN)
dp = Dispatcher()

PRICE = LabeledPrice(label="Acesso ao Grupo de Nudes", amount=150)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Para pagar, clique no botão abaixo.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💰 Pagar", callback_data="pay")]]))

@dp.callback_query(F.data == "pay")
async def send_invoice(callback):
    await bot.send_invoice(callback.from_user.id, "Acesso Nudes", "Acesso ao grupo", "nudes_access", "", "XTR", [PRICE])
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre):
    await bot.answer_pre_checkout_query(pre.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    if GROUP_ID:
        invite = await bot.create_chat_invite_link(GROUP_ID, member_limit=1)
        await message.answer(f"✅ Link: {invite.invite_link}")
    else:
        await message.answer("Grupo não configurado.")

@dp.message(Command("id"))
async def get_id(message: Message):
    await message.answer(f"ID do grupo: {message.chat.id}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
