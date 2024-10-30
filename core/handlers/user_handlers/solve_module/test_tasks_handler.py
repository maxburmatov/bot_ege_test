from aiogram import Router, Bot, F

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.database.metods.change_student import add_points, add_test, add_daily_temp
from core.database.metods.check_student import check_use_boost, check_daily_test
from core.database.metods.solve_student import get_random_tasks
from core.database.metods.stats_student import add_stat_tasks
from core.keyboards.reply import back_menu, next_task, tasks_selection_menu, next_task_in_test, view_results, \
    results_menu, back_solve

from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_POINTS, LEXICON_STICKERS
from core.states.states import StateTest
from core.utils.functions import get_task_completion_time, get_int_time, delete_message
import asyncio

router = Router()

list_tasks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

@router.message(F.text == LEXICON_BUTTON["test"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("[1] Планиметрия\n"
                         "[2] Векторы\n"
                         "[3] Стереометрия\n"
                         "[4] Начала теории вероятностей\n"
                         "[5] Вероятности сложных событий\n"
                         "[6] Простейшие уравнения\n"
                         "[7] Вычисления и преобразования\n"
                         "[8] Производная и первообразная\n"
                         "[9] Задачи с прикладным содержанием\n"
                         "[10] Текстовые задачи\n"
                         "[11] Графики функций\n"
                         "[12] Наибольшее и наименьшее значение функций\n\n"
                         "🤖: Выбери номер задания чтобы пройти по нему тест!",
                         reply_markup=tasks_selection_menu)

    await state.set_state(StateTest.TASK_SELECTED)

@router.message(StateFilter(StateTest.TASK_SELECTED),
                F.text.in_(list_tasks))
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    if await check_daily_test(message.from_user.id):
        number_task = message.text
        await add_test(message.from_user.id)
        data_tasks = await get_random_tasks(int(number_task), "test")

        task = data_tasks[0]
        counter = 1

        await state.update_data(data_tasks=data_tasks)
        await state.update_data(new_data_tasks=[])
        await state.update_data(counter=counter)

        caption = f"ID#{task["id"]} [{counter}/5]\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):"
        await bot.send_photo(message.chat.id, task["photo_task"], caption=caption, reply_markup=back_solve)

        await state.set_state(StateTest.CHECK_ANSWER)
    else:
        await message.answer("🤖: На сегодня тесты закончились! Жду тебя завтра!\n\n"
                             "Если хочешь прорешивать больше тестов в день, то активируй подписку!")
        await state.clear()

@router.message(StateFilter(StateTest.TASK_SELECTED),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Нeт такого задания!", reply_markup=tasks_selection_menu)
@router.message(StateFilter(StateTest.CHECK_ANSWER),
                F.content_type.in_({'text'}),
                (F.text.regexp(r"^(\d+)[.](\d+)$")) | (F.text.regexp(r"^(\d+)$"))
                )
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    state_data = await state.get_data()
    user_answer = message.text
    data_tasks = state_data["data_tasks"]
    new_data_tasks = state_data["new_data_tasks"]
    counter = state_data["counter"]

    task = data_tasks[0]
    task["user_answer"] = float(user_answer)
    new_data_tasks.append(task)
    await state.update_data(new_data_tasks=new_data_tasks)
    if counter == 5:
        await message.answer(
            f"🤖: Тест завершен, можно посмотреть результаты!",
            reply_markup=view_results)
        await state.set_state(StateTest.TEST_END)
    else:
        text = "🤖: Ответ принят! Идем дальше?"
        await message.answer(text, reply_markup=next_task_in_test)
        await state.set_state(StateTest.NEXT_TASK)


@router.message(StateFilter(StateTest.CHECK_ANSWER),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    state_data = await state.get_data()
    data_tasks = state_data["data_tasks"]
    counter = state_data["counter"]
    task = data_tasks[0]
    caption = f"ID#{task["id"]} [{counter}/5]\n\n🤖: Упс! Ответ состоит только из цифр и десятичных дробей (например: 2.5). Напиши ответ еще раз!"
    await bot.send_photo(message.chat.id, task["photo_task"], caption=caption, reply_markup=back_solve)

    await state.set_state(StateTest.CHECK_ANSWER)


@router.message(StateFilter(StateTest.NEXT_TASK),
                F.text == LEXICON_BUTTON["next_task"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    state_data = await state.get_data()
    data_tasks = state_data["data_tasks"]
    data_tasks.pop(0)

    counter = state_data["counter"]
    counter = counter + 1

    task = data_tasks[0]
    await state.update_data(counter=counter)

    caption = f"ID#{task["id"]} [{counter}/5]\n\n🤖: Напиши ответ без пробелов, десятичные дроби через точку (например: 2.5):"
    await bot.send_photo(message.chat.id, task["photo_task"], caption=caption, reply_markup=back_solve)

    await state.set_state(StateTest.CHECK_ANSWER)

@router.message(StateFilter(StateTest.NEXT_TASK),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Выбери нужное действие!")


@router.message(StateFilter(StateTest.TEST_END),
                F.text == LEXICON_BUTTON["view_results"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    state_data = await state.get_data()
    new_data_tasks = state_data["new_data_tasks"]
    text, points_text, points, sticker = await check_answer_task(message.from_user.id, new_data_tasks)
    await add_points(message.from_user.id, points)
    await bot.send_sticker(message.from_user.id, sticker)
    await message.answer(f"{text}\n\n{points_text}", reply_markup=results_menu)


@router.message(StateFilter(StateTest.TEST_END),
                F.text != LEXICON_BUTTON["back_menu"])
async def info_random_task(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Выбери нужное действие!")


async def check_answer_task(tg_id, new_data_tasks):

    points = 0
    true_tasks = 0
    table_answer = 'Твой ответ (Правильный)\n\n'

    for counter, task in enumerate(new_data_tasks, 1):
        if task["answer"] == task["user_answer"]:
            true_tasks += 1
            table_answer += f'✅ {counter}) {task["user_answer"]} ({task["answer"]})\n'
            await add_stat_tasks(tg_id, task["number_task"], 1)
        else:
            table_answer += f'❌ {counter}) {task["user_answer"]} ({task["answer"]})\n'
            await add_stat_tasks(tg_id, task["number_task"], 0)

    results_text = f"🤖: Тест завершен! Правильных ответов {true_tasks} из 5\n\n"

    percent_completion = true_tasks / 5 * 100
    task = new_data_tasks[0]
    await add_daily_temp(tg_id, "test", task["number_task"], 1, int(percent_completion))

    match true_tasks:
        case 5:
            points = 12
            sticker = LEXICON_STICKERS["score5"]
        case 4:
            points = 8
            sticker = LEXICON_STICKERS["score4"]
        case 3:
            points = 6
            sticker = LEXICON_STICKERS["score3"]
        case 2:
            points = 4
            sticker = LEXICON_STICKERS["score2"]
        case 1:
            points = 2
            sticker = LEXICON_STICKERS["score1"]
        case 0:
            points = 0
            sticker = LEXICON_STICKERS["score0"]

    points_boost = ""

    if await check_use_boost(tg_id):
        points *= 2
        points_boost = " Множитель опыта активен!"

    points_text = f"Получено: 🔷 {points}!" + points_boost

    text = results_text + table_answer

    return text, points_text, points, sticker