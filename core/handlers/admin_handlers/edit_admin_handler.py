from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.utils.deep_linking import create_start_link
from core.database.admin_metods import admin_add_task_database, get_task_info, admin_edit_task_database
from core.database.metods.get_student import get_count_invite
from core.filters.user_filters import IsAdmin

from core.keyboards.reply_admin import get_admin_panel, admin_edit_menu
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.states.states import StateAdminAddTask, StateAdminEditTask
from core.utils.functions import delete_message

router = Router()


@router.message(F.text == LEXICON_BUTTON["admin_edit"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Выбери нужное действие!", reply_markup=admin_edit_menu)

@router.message(F.text == LEXICON_BUTTON["admin_add_task"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Напиши номер задания и прикрепи фото задания:")
    await state.set_state(StateAdminAddTask.ADD_TASK)

@router.message(StateFilter(StateAdminAddTask.ADD_TASK), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    number = message.caption
    number = int(number)
    photo_task = message.photo[-1].file_id
    await state.update_data(photo_task=photo_task)
    await state.update_data(number=number)

    await message.answer("🤖: Напиши ответ и прикрепи фото решения")

    await state.set_state(StateAdminAddTask.ADD_ANSWER)

@router.message(StateFilter(StateAdminAddTask.ADD_ANSWER), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):
    await delete_message(message, message.chat.id, message.message_id)

    answer = message.caption
    answer = float(answer)
    photo_answer = message.photo[-1].file_id
    data = await state.get_data()

    await admin_add_task_database(data.get("number"), data.get("photo_task"), photo_answer, answer)

    await message.answer(f"🤖: Задание успешно добавлено!", reply_markup=admin_edit_menu)

    await state.clear()

@router.message(F.text == LEXICON_BUTTON["admin_edit_task"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Напиши ID задания:")
    await state.set_state(StateAdminEditTask.CHECK_TASK)

@router.message(StateFilter(StateAdminEditTask.CHECK_TASK), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    task_id = message.text
    task_info = await get_task_info(int(task_id))
    await state.update_data(task_id=int(task_id))

    await bot.send_photo(message.chat.id, task_info.get("photo_task"))
    await message.answer(f"ID#{task_info.get("id")} №{task_info.get("number_task")} Ответ: {task_info.get("answer")}\n"
                         f"is_week = {task_info.get("is_week")}| is_daily = {task_info.get("is_daily")}\n")
    await bot.send_photo(message.chat.id, task_info.get("photo_answer"))

    await message.answer("🤖: Напиши номер задания и прикрепи фото задания:")
    await state.set_state(StateAdminEditTask.ADD_TASK)

@router.message(StateFilter(StateAdminEditTask.ADD_TASK), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    number = message.caption
    number = int(number)
    photo_task = message.photo[-1].file_id
    await state.update_data(photo_task=photo_task)
    await state.update_data(number=number)

    await message.answer("🤖: Напиши ответ и прикрепи фото решения")

    await state.set_state(StateAdminEditTask.ADD_ANSWER)

@router.message(StateFilter(StateAdminEditTask.ADD_ANSWER), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    answer = message.caption
    answer = float(answer)
    photo_answer = message.photo[-1].file_id
    data = await state.get_data()

    await admin_edit_task_database(data.get("task_id"), data.get("number"), data.get("photo_task"), photo_answer, answer)

    await message.answer(f"🤖: Задание успешно изменено!", reply_markup=admin_edit_menu)

    await state.clear()