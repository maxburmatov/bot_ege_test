from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.utils.deep_linking import create_start_link
from core.database.admin_metods import admin_add_task_database, get_task_info, admin_edit_task_database
from core.database.metods.get_student import get_count_invite, get_daily_temp
from core.database.metods.quests import generate_daily_quests
from core.filters.user_filters import IsAdmin

from core.keyboards.reply_admin import get_admin_panel, admin_edit_menu, main_menu_keyboard_admin
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.states.states import StateAdminAddTask, StateAdminEditTask
from core.utils.functions import delete_message

router = Router()

@router.message((F.text == LEXICON_BUTTON["back_menu"]) | (F.text == "/menu"),
                IsAdmin()
                )
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await state.clear()
    await bot.send_sticker(message.from_user.id,
                           "CAACAgIAAxkBAAJShWU8wyWkZ6vYvm3qKHDWmwhsghZ5AAI0DAAC6QiISlc3ARD4weYnMAQ")
    await message.answer("🤖: Выбери нужный раздел!", reply_markup=await main_menu_keyboard_admin())


@router.message((F.text == LEXICON_BUTTON["admin_panel"]) | (F.text == LEXICON_BUTTON["back_admin_panel"]), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Ты в меню админа!", reply_markup=await get_admin_panel())

@router.message(F.text == "/test", IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    count_all, count_all_r = await get_daily_temp(message.chat.id, "task", 7)