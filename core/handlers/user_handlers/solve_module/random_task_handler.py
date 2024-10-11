from aiogram import Router, Bot, F

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.database.metods.change_student import add_task, add_points, add_time_tasks
from core.database.metods.check_student import check_daily_tasks, check_use_boost
from core.database.metods.solve_student import get_random_tasks
from core.keyboards.reply import back_menu, next_task

from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_POINTS
from core.states.states import StateRandomTask
from core.utils.functions import get_task_completion_time, get_int_time

router = Router()

@router.message(F.text == LEXICON_BUTTON["random_task"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):
    if await check_daily_tasks(message.from_user.id):
        first_try = 1

        await add_task(message.from_user.id)
        data_tasks = await get_random_tasks(0, "task")

        task = data_tasks[0]
        caption = f"ID#{task["id"]} Задание №{task["number_task"]}"
        await bot.send_photo(message.chat.id, task["photo_task"])

        await state.update_data(data_tasks=data_tasks)
        await state.update_data(first_try=1)

        await message.answer(
            f"ID#{task["id"]} Задание №{task["number_task"]}\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):",
            reply_markup=back_menu)

        begin_time = await get_int_time(message.date)
        await state.update_data(begin_time=begin_time)

        await state.set_state(StateRandomTask.CHECK_ANSWER)
    else:
        await message.answer("🤖: На сегодня задания закончились! Жду тебя завтра!\n\n"
                             "Если хочешь прорешивать больше заданий в день, то активируй подписку!")
        await state.clear()
    await message.delete()


@router.message(StateFilter(StateRandomTask.CHECK_ANSWER),
                F.content_type.in_({'text'}),
                (F.text.regexp(r"^(\d+)[.](\d+)$")) | (F.text.regexp(r"^(\d+)$"))
                )
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    user_answer = message.text
    end_time = await get_int_time(message.date)

    text, points = await check_answer_task(message.from_user.id, state_data, user_answer, end_time)

    await message.answer(text, reply_markup=next_task)
    await add_points(message.from_user.id, points)
    await state.set_state(StateRandomTask.NEXT_TASK)


@router.message(StateFilter(StateRandomTask.NEXT_TASK),
                F.text == LEXICON_BUTTON["resolve_task"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    first_try = 0
    await state.update_data(first_try=first_try)

    data = await state.get_data()
    data_tasks = data["data_tasks"]
    task = data_tasks[0]

    caption = f"ID#{task["id"]} Задание №{task["number_task"]}"
    await bot.send_photo(message.chat.id, task["photo_task"])

    await message.answer(
        f"ID#{task["id"]} Задание №{task["number_task"]}\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):",
        reply_markup=back_menu)

    begin_time = await get_int_time(message.date)
    await state.update_data(begin_time=begin_time)

    await state.set_state(StateRandomTask.CHECK_ANSWER)


@router.message(StateFilter(StateRandomTask.NEXT_TASK),
                F.text == LEXICON_BUTTON["check_solution"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    data_tasks = data["data_tasks"]
    task = data_tasks[0]

    await bot.send_photo(message.chat.id, task["photo_answer"])

    await state.set_state(StateRandomTask.NEXT_TASK)

@router.message(StateFilter(StateRandomTask.NEXT_TASK),
                F.text == LEXICON_BUTTON["next_task"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    data_tasks = data["data_tasks"]
    data_tasks.pop(0)

    if await check_daily_tasks(message.from_user.id):
        task = data_tasks[0]
        caption = f"ID#{task["id"]} Задание №{task["number_task"]}"
        await bot.send_photo(message.chat.id, task["photo_task"])

        await state.update_data(data_tasks=data_tasks)
        await state.update_data(first_try=1)

        await message.answer(
            f"ID#{task["id"]} Задание №{task["number_task"]}\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):",
            reply_markup=back_menu)

        begin_time = await get_int_time(message.date)
        await state.update_data(begin_time=begin_time)

        await state.set_state(StateRandomTask.CHECK_ANSWER)
    else:
        await message.answer("🤖: На сегодня задания закончились! Жду тебя завтра!\n\n"
                             "Если хочешь прорешивать больше заданий в день, то активируй подписку!")
        await state.clear()


@router.message(StateFilter(StateRandomTask.CHECK_ANSWER),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        f"Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5)",
        reply_markup=back_menu)
    await state.set_state(StateRandomTask.CHECK_ANSWER)

@router.message(StateFilter(StateRandomTask.NEXT_TASK),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):
    await message.answer("🤖: Выбери нужное действие!")


async def check_answer_task(tg_id, state_data, user_answer, end_time):
    data_tasks = state_data['data_tasks']
    first_try = state_data['first_try']
    begin_time = state_data['begin_time']

    time_answer = end_time - begin_time
    task = data_tasks[0]
    task_answer = task["answer"]
    text = ""
    points = 0
    bot_time_answer = await get_task_completion_time(time_answer)

    if first_try == 1:
        if float(user_answer) == task_answer:
            points = LEXICON_POINTS["random_task_plus"]
            points_text = f"Получено: 🔷 {points}"

            if await check_use_boost(tg_id):
                points = points * 2
                points_text = f"Получено: 🔷 {points}, множитель опыта активен!"

            text += f"🤖: ✅ Верно! {points_text}"
        else:
            points = LEXICON_POINTS["random_task_minus"]

            text += f"🤖: ❌ Не верно! Я забрал у тебя 🔷 {abs(points)}!"

        await add_time_tasks(tg_id, time_answer)
    else:
        if float(user_answer) == task_answer:
            text += "🤖: ✅ Верно! Баллы начисляются только за первую попытку решения задания!"
        else:
            text += "🤖: ❌ Не верно! Баллы снимаются только за первую попытку решения задания!"

    text += f"\n\n{bot_time_answer}"

    return text, points
