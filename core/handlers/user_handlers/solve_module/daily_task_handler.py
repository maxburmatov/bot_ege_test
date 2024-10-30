from aiogram import Router, Bot, F

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.database.metods.change_student import add_task, add_points, add_time_tasks, add_solve_daily_task
from core.database.metods.check_student import check_solve_daily_task, check_use_boost
from core.database.metods.solve_student import get_daily_task
from core.keyboards.reply import back_menu, begin_solve_menu, back_solve, end_daily_task

from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_POINTS
from core.states.states import StateDailyTask
from core.utils.functions import get_task_completion_time, get_int_time, delete_message

router = Router()


@router.message(F.text == LEXICON_BUTTON["begin_solve"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await add_solve_daily_task(message.from_user.id, 1)
    await add_task(message.from_user.id)

    task = await get_daily_task()
    await state.update_data(task=task)

    caption = f"ID#{task["id"]} Задание №{task["number_task"]}\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):"
    await bot.send_photo(message.chat.id, task["photo_task"], caption=caption, reply_markup=back_solve)

    begin_time = await get_int_time(message.date)
    await state.update_data(begin_time=begin_time)
    await state.set_state(StateDailyTask.CHECK_ANSWER)


@router.message(StateFilter(StateDailyTask.CHECK_ANSWER),
                (F.text.regexp(r"^(\d+)[.](\d+)$")) | (F.text.regexp(r"^(\d+)$"))
                )
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    state_data = await state.get_data()
    user_answer = message.text
    end_time = await get_int_time(message.date)

    text, points = await check_answer_task(message.from_user.id, state_data, user_answer, end_time)

    await message.answer(text, reply_markup=end_daily_task)
    await add_points(message.from_user.id, points)
    await state.set_state(StateDailyTask.END_DAILY_TASK)


@router.message(StateFilter(StateDailyTask.END_DAILY_TASK),
                F.text == LEXICON_BUTTON["check_solution"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    data = await state.get_data()
    task = data["task"]

    await bot.send_photo(message.chat.id, task["photo_answer"],reply_markup=back_solve)


@router.message(StateFilter(StateDailyTask.CHECK_ANSWER),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(
        f"Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5)",
        reply_markup=back_solve)
    await state.set_state(StateDailyTask.CHECK_ANSWER)

@router.message(StateFilter(StateDailyTask.END_DAILY_TASK),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await bot.delete_message(message.chat.id, message.message_id - 1)

    await message.answer("🤖: Выбери нужное действие!", reply_markup=end_daily_task)


async def check_answer_task(tg_id, state_data, user_answer, end_time):
    task = state_data['task']
    begin_time = state_data['begin_time']

    time_answer = end_time - begin_time
    task_answer = task["answer"]
    text = ""
    points = 0
    bot_time_answer = await get_task_completion_time(time_answer)

    if float(user_answer) == task_answer:
        points = LEXICON_POINTS["daily_task_plus"]
        points_text = f"Получено: 🔷 {points}"

        if await check_use_boost(tg_id):
            points = points * 2
            points_text = f"Получено: 🔷 {points}, множитель опыта активен!"

        text += f"🤖: ✅ Верно! {points_text}"

        await add_solve_daily_task(tg_id, 2)
    else:
        points = LEXICON_POINTS["daily_task_minus"]

        text += f"🤖: ❌ Не верно! Я забрал у тебя 🔷 {abs(points)}!"

    await add_time_tasks(tg_id, time_answer)

    text += f"\n\n{bot_time_answer}"

    return text, points




