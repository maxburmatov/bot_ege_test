__all__ = ("router",)

import asyncio

from aiogram import Router, Bot, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.reply import solve_menu, solve_tasks_menu, solve_variants_menu

from core.lexicon.lexicon import LEXICON_BUTTON

router = Router(name=__name__)

@router.message((F.text == LEXICON_BUTTON["solve"]) | (F.text == LEXICON_BUTTON["back"]))
async def info_random_task(message: Message, state: FSMContext, bot: Bot):
    await message.answer("🤖: Что будем решать?", reply_markup=solve_menu)
    await message.delete()

@router.message(F.text == LEXICON_BUTTON["solve_tasks"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):
    await message.answer("🤖: Решаем задания или проходим тест?", reply_markup=solve_tasks_menu)
    await message.delete()

@router.message(F.text == LEXICON_BUTTON["solve_variant"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):
    await message.answer("🤖: Какой вариант решаем?", reply_markup=solve_variants_menu)
    await message.delete()

