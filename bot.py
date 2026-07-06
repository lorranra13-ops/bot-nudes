import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1004260845425   # Seu ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Planos de pagamento
PLANS = {
    "1": {"title": "Acesso 1 Mês", "price": 100, "desc": "Acesso por 30 dias"},
    "2": {"title": "Acesso Vitalício", "price": 250, "desc": "Acesso para sempre"}
}

@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 Mês - 100 Stars", callback_data="plan_1")],
        [InlineKeyboardButton(text="Vitalício - 250 Stars", callback_data="plan_2")]
    ])
    await message.answer("Escolha seu plano de acesso ao grupo de nudes:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("plan_"))
async def send_payment(callback):
    plan_id = callback.data.split("_")[1]
    plan = PLANS[plan_id]
    
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=plan["title"],
        description=plan["desc"],
        payload=f"access_{plan_id}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=plan["title"], amount=plan["price"])]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre):
    await bot.answer_pre_checkout_query(pre.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        invite = await bot.create_chat_invite_link(GROUP_ID, member_limit=1, expire_date=None)
        await message.answer(f"✅ Pagamento confirmado!\n\n🔗 Link de acesso:\n{invite.invite_link}\n\nNão compartilhe!")
    except Exception as e:
        await message.answer("Erro ao gerar link. Contate o administrador.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
