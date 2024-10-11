from aiogram import Router, Bot, F
from aiogram.types import Message

from aiogram.utils.deep_linking import create_start_link
from core.database.metods.get_student import get_count_invite

from core.keyboards.reply import info_menu
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS

router = Router()

@router.message(F.text == LEXICON_BUTTON["info"])
async def info(message: Message, bot: Bot):
    await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["info"])
    await message.answer("🤖: Что хочешь посмотреть?", reply_markup=info_menu)
    await message.delete()

@router.message(F.text == LEXICON_BUTTON["invite_friends"])
async def invite_friends(message: Message, bot: Bot):
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    count_invite_friends = await get_count_invite(message.from_user.id)
    answer_invite = await message_invite(count_invite_friends)

    await message.answer(f"🤖: Твою ссылку для приглашений отправил ниже! Скопируй и отправь друзьям!")
    await message.answer(link)
    await message.answer(answer_invite, reply_markup=info_menu)




async def message_invite(count_invite_friends):
    if count_invite_friends == 0:
        str_invite = f"🤖: Пока что у тебя нет приглашений :("
    elif count_invite_friends < 5:
        str_invite = f"🤖: Ты пригласил {count_invite_friends} друга!"
    else:
        str_invite = f"🤖: Ты пригласил {count_invite_friends} друзей!"

    return str_invite
