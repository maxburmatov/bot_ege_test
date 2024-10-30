from aiogram import Bot
from aiogram.types import Message, LabeledPrice, CallbackQuery, PreCheckoutQuery
from core.database.metods.backpack_student import add_item_in_backpack
from core.lexicon.lexicon import LEXICON_STICKERS

async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_pay(message: Message, bot: Bot):

    if message.successful_payment.invoice_payload == "buy_avatars_case_1":
        await add_item_in_backpack(message.from_user.id, 20, 1)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x1 кейс в твой рюкзак!")

    if message.successful_payment.invoice_payload == "buy_avatars_case_5":
        await add_item_in_backpack(message.from_user.id, 20, 5)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x5 кейсов в твой рюкзак!")

    if message.successful_payment.invoice_payload == "buy_avatars_case_20":
        await add_item_in_backpack(message.from_user.id, 20, 20)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x20 кейсов в твой рюкзак!")

    if message.successful_payment.invoice_payload == "buy_avatars_case_premium_1":
        await add_item_in_backpack(message.from_user.id, 22, 1)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x1 кейс в твой рюкзак!")

    if message.successful_payment.invoice_payload == "buy_avatars_case_premium_5":
        await add_item_in_backpack(message.from_user.id, 22, 5)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x5 кейсов в твой рюкзак!")

    if message.successful_payment.invoice_payload == "buy_avatars_case_premium_5":
        await add_item_in_backpack(message.from_user.id, 22, 20)
        await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["payment"])
        await message.answer("🤖: Добавил x20 кейсов в твой рюкзак!")
