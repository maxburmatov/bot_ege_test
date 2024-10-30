__all__ = ("router",)

import asyncio

from aiogram import Router, Bot, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.database.metods.check_student import check_solve_daily_task
from core.keyboards.reply import solve_menu, solve_tasks_menu, solve_variants_menu, begin_solve_menu, back_solve, \
    solve_menu_keyboard, theory_menu_keyboard

from core.lexicon.lexicon import LEXICON_BUTTON
from core.utils.functions import delete_message

router = Router(name=__name__)

@router.message((F.text == LEXICON_BUTTON["solve"]) | (F.text == LEXICON_BUTTON["back_solve"]) | (F.text == "/solve")
                )
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await state.clear()

    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(1)

    await message.answer("🤖: Что будем решать?", reply_markup=await solve_menu_keyboard())

@router.message(F.text == LEXICON_BUTTON["solve_tasks"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(1)

    await message.answer("🤖: Решаем задания или проходим тест?", reply_markup=solve_tasks_menu)


@router.message(F.text == LEXICON_BUTTON["solve_variant"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(1)

    await message.answer("🤖: Какой вариант решаем?", reply_markup=solve_variants_menu)

@router.message(F.text == LEXICON_BUTTON["solve_daily_task"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(1)

    if await check_solve_daily_task(message.from_user.id):
        await message.answer(f"🤖: Здесь я каждый день добавляю случайное задание из всей базы данных!",
                             reply_markup=begin_solve_menu)
    else:
        await message.answer("🤖: У тебя уже пройдено задание дня! Жду тебя завтра!", reply_markup=back_solve)


@router.message(F.text == LEXICON_BUTTON["solve_theory"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(1)

    await message.answer("🤖: Выбери какую теорию хочешь посмотреть!", reply_markup=await theory_menu_keyboard())



