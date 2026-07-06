import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1004260845425
PIX_CHAVE = 46394612839   # ← Troque pela sua chave PIX

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Pagar via PIX", callback_data="pix")
    ]])
    await message.answer(
        "💰 Para ter acesso ao grupo:\n\n"
        f"Chave PIX: <code>{PIX_CHAVE}</code>\n\n"
        "Valor sugerido: R$ 20\n\n"
        "Após pagar, envie o comprovante aqui.",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "pix")
async def pix_info(callback):
    await callback.message.answer(
        "✅ Envie o comprovante do PIX aqui (foto ou print) que eu libero seu acesso manualmente."
    )
    await callback.answer()

@dp.message(F.photo | F.document)  # Quando receber foto ou arquivo (comprovante)
async def receive_proof(message: Message):
    await message.answer("✅ Comprovante recebido! Aguarde a liberação (geralmente em até 5 minutos).")
    # Aqui você receberia notificação e liberaria manualmente

    # Liberar automaticamente (temporário)
    try:
        invite = await bot.create_chat_invite_link(GROUP_ID, member_limit=1)
        await message.answer(f"🔗 Link de acesso:\n{invite.invite_link}")
    except:
        pass

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
