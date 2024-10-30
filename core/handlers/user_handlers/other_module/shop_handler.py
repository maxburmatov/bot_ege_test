from aiogram import F, Router, Bot
from aiogram.types import Message

from core.database.metods.shop import get_shop_case

from core.keyboards.inline_shop import get_shop_cases_keyboard
from core.keyboards.reply import shop_menu
from core.lexicon.lexicon import LEXICON_BUTTON
from core.utils.functions import delete_message

router = Router()

@router.message((F.text == LEXICON_BUTTON["shop"]) | (F.text == "/shop")
                )
async def backpack_page_handler(message: Message,  bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: В магазине можно купить кейсы за ⭐️ Telegram Stars, "
                         "а также приобрести особые предметы за звезды лидера!", reply_markup=shop_menu)


@router.message(F.text == LEXICON_BUTTON["shop_cases"])
async def backpack_page_handler(message: Message,  bot: Bot):

    await message.delete()

    count_cases, info_case = await get_shop_case(0)
    cases_data = info_case["cases_data"]
    case = cases_data[0]
    title_case = case[1]
    image_case = case[3]

    caption = f"Ты выбрал: {title_case}"
    keyboard = await get_shop_cases_keyboard()  # Page: 0

    msg = await bot.send_photo(
        chat_id=message.chat.id,
        photo=image_case,
        caption=caption,
        reply_markup=keyboard
    )