import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1000000000000  # ← TROQUE pelo ID do seu grupo

bot = Bot(token=TOKEN)
dp = Dispatcher()

PRICE = LabeledPrice(label="Acesso ao Grupo de Nudes", amount=150)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🔥 Bem-vindo!\n\nPara ter acesso ao grupo de nudes, clique abaixo:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="💰 Liberar Acesso", callback_data="pay")
        ]])
    )

@dp.callback_query(F.data == "pay")
async def send_invoice(callback):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Acesso ao Grupo de Nudes",
        description="Acesso vitalício",
        payload="nudes_access",
        provider_token="",
        currency="XTR",
        prices=[PRICE]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre):
    await bot.answer_pre_checkout_query(pre.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        invite = await bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1
        )
        await message.answer(f"✅ Pagamento OK!\n\nLink: {invite.invite_link}")
    except Exception:
        await message.answer("Erro ao gerar link.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
