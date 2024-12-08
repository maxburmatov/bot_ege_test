from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from core.database.metods.admin_metods import admin_add_task_database
from core.filters.user_filters import IsAdmin

from core.keyboards.reply_admin import get_admin_panel, main_menu_keyboard_admin
from core.lexicon.lexicon import LEXICON_BUTTON
from core.services.admin_create_image_task import create_image_task
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

    list_tasks = await create_image_task()
    for task in list_tasks:
        task_image = FSInputFile(task["task_image"])
        answer_image = FSInputFile(task["answer_image"])

        send_task = await message.answer_photo(task_image)
        print(send_task)
        photo_id_task = send_task.photo[-1].file_id
        print(photo_id_task)
        send_answer = await message.answer_photo(answer_image)
        photo_id_answer = send_answer.photo[-1].file_id
        print(photo_id_answer)

        await admin_add_task_database(int(task["number"]), photo_id_task, photo_id_answer, task["answer"])



