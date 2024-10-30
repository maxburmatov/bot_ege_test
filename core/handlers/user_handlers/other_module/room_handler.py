import os
import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from re import compile

from core.database.metods.backpack_student import get_image_avatar_profile
from core.database.metods.change_student import change_name
from core.database.metods.get_student import get_info_student
from core.database.metods.quests import get_count_quests_completed
from core.database.metods.stats_student import get_daily_stats_student, get_general_stats_student
from core.database.metods.sub_student import get_status_sub
from core.database.metods.table_leaders import get_info_student_league
from core.keyboards.reply import room_menu, room_settings_menu
from core.lexicon.bad_words import check_bad_words
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.services.create_image import create_room_image
from core.states.states import StateChangeName
from core.utils.functions import delete_message

router = Router(name=__name__)

@router.message((F.text == LEXICON_BUTTON["my_room"]) | (F.text == LEXICON_BUTTON["back_room"]) | (F.text == "/room")
                )
async def my_room(message: Message, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    info_student, stats_daily_student, stats_general_student, info_league = await table_profile_stats(message.from_user.id)

    image_room = await create_room_image(info_student, stats_daily_student, stats_general_student, info_league)
    image = FSInputFile(image_room)

    await message.answer("🤖: Секундочку! Перемещаю тебя в комнату...")
    await asyncio.sleep(1)
    await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["transfer"])
    await bot.send_chat_action(message.chat.id, action="upload_photo")
    await asyncio.sleep(2)

    await message.answer_photo(image)
    os.remove(image_room)

    await message.answer("🤖: Здесь можно посмотреть информацию о профиле и свою статистику, а также настроить профиль!", reply_markup=room_menu)


@router.message(F.text == LEXICON_BUTTON["room_settings"])
async def room_settings(message: Message):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Здесь можно поменять имя и цель по баллам ЕГЭ!", reply_markup=room_settings_menu)


@router.message(F.text == LEXICON_BUTTON["change_name"])
async def room_settings(message: Message, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Напиши новое имя или никнейм:", reply_markup=room_settings_menu)
    await state.set_state(StateChangeName.CHANGE_NAME)

@router.message(StateFilter(StateChangeName.CHANGE_NAME))
async def room_settings(message: Message, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    name = message.text
    regex = "^[0-9a-zA-Zа-яА-ЯёЁ_]+$"
    pattern = compile(regex)

    if len(name) <= 12 and pattern.search(name) is not None and await check_bad_words(name):
        await change_name(message.from_user.id, name)
        await message.answer(f"🤖: Имя успешно изменено! Теперь твое имя: {name}", reply_markup=room_settings_menu)
        await state.clear()
    else:
        await message.answer(
            f"🤖: Не принимаю такое имя! Длина должна быть не больше 12 символов, а также можно использовать только буквы, цифры и нижнее подчеркивание!",
            reply_markup=room_settings_menu)
        await message.answer(f"🤖: Напиши новое имя или никнейм:",
                             reply_markup=room_settings_menu)
        await state.set_state(StateChangeName.CHANGE_NAME)

async def table_profile_stats(tg_id):

    info_student = await get_info_student(tg_id)
    info_student["avatar_image"] = await get_image_avatar_profile(info_student['avatar_id'])
    info_student["status_sub"] = await get_status_sub(tg_id)
    info_student["count_quests"] = await get_count_quests_completed(tg_id)

    stats_daily_student = await get_daily_stats_student(tg_id)
    stats_general_student = await get_general_stats_student(tg_id)

    info_league = await get_info_student_league(tg_id)

    return info_student, stats_daily_student, stats_general_student, info_league