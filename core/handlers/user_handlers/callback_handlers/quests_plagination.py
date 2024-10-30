import os

from random import choices, randint, uniform

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from re import findall

from core.database.metods.backpack_student import get_title_item, add_item_in_backpack
from core.database.metods.change_student import add_points, update_collect_daily_bonus
from core.database.metods.check_student import check_collect_daily_bonus, check_invite
from core.database.metods.get_student import get_count_invite, get_daily_temp, get_days_daily_bonus, get_league_id
from core.database.metods.quests import check_generate_daily_quests, get_daily_quests, generate_daily_quests, \
    check_quest_completed, add_quest_completed, check_generate_other_quests, generate_other_quests, get_other_quests, \
    add_student_quest, delete_student_quest
from core.keyboards.inline_quests import get_main_quests_keyboard, QuestsCallback, QuestsCategory, QuestsAction, \
    get_quests_keyboard, get_daily_bonus_keyboard
from core.keyboards.reply import main_menu, back_menu
from core.lexicon.lexicon import LEXICON_BUTTON
from core.utils.functions import delete_message

router = Router()


@router.message((F.text == LEXICON_BUTTON["quests"]) | (F.text == "/quests"))
async def backpack_page_handler(message: Message, bot: Bot):
    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(
        "🤖: Здесь можно посмотреть доступные тебе квесты, за их выполнение можно получить различные награды!",
        reply_markup=back_menu)
    keyboard = await get_main_quests_keyboard()  # Page: 0
    text = f"🤖: Выбери какие квесты хочешь посмотреть и не забудь про ежедневный бонус!"

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )


@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.daily_bonus),
    QuestsCallback.filter(F.action == QuestsAction.skip)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    text = f"🤖: Подкинул тебе заданий на сегодня!\n\n"

    days_in_row, daily_bonus_by_day = await get_days_daily_bonus(query.from_user.id)

    text = await message_daily_bonus(days_in_row, daily_bonus_by_day)

    keyboard = await get_daily_bonus_keyboard()

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def message_daily_bonus(days_in_row, daily_bonus_by_day):
    table = ""
    if days_in_row == 0:
        for i in range(1, 8):
            table += f'☑️ {i} день - ?\n'
    else:
        for i in range(1, 8):
            daily_bonus = daily_bonus_by_day[f"{str(i)}"]
            if i <= days_in_row:
                table += f'✅ {i} день - 🔷 {daily_bonus} \n'
            else:
                table += f'☑️ {i} день - ?\n'

    return table


@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.daily_bonus),
    QuestsCallback.filter(F.action == QuestsAction.collect_bonus)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    days_in_row, daily_bonus_by_day = await get_days_daily_bonus(query.from_user.id)

    if await check_collect_daily_bonus(query.from_user.id):
        text = f"🤖: Ты уже получил ежедневный бонус сегодня, приходи завтра!"
    else:
        daily_bonus = daily_bonus_by_day[f"{str(days_in_row + 1)}"]
        text = (f"🤖: Ежедневный бонус собран!\n\n"
                f"Тебе начислено: 🔷 {daily_bonus}!")
        await update_collect_daily_bonus(query.from_user.id)
        await add_points(query.from_user.id, daily_bonus)

        text_change = await message_daily_bonus(days_in_row + 1, daily_bonus_by_day)
        keyboard = await get_daily_bonus_keyboard()
        await query.message.edit_text(
            text=text_change,
            reply_markup=keyboard
        )

    await query.answer(text=text, show_alert=True)


@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.daily_quests),
    QuestsCallback.filter(F.action == QuestsAction.skip)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    text = f"🤖: Подкинул тебе заданий на сегодня!\n\n"

    if await check_generate_daily_quests(query.from_user.id):
        quests = await get_daily_quests(query.from_user.id)
    else:
        quests = await generate_daily_quests(query.from_user.id)

    text = text + await message_quests(query.from_user.id, quests, "daily")

    keyboard = await get_quests_keyboard("daily")

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.daily_quests),
    QuestsCallback.filter(F.action == QuestsAction.check_execution)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    quests = await get_daily_quests(query.from_user.id)
    text = await execution_daily_quests_completed(query.from_user.id, quests, "daily")

    await query.answer(text=text, show_alert=True)

    if text != "🤖: Пока нет обновлений!":
        keyboard = await get_quests_keyboard("daily")
        text = f"🤖: Подкинул тебе заданий на сегодня!\n\n"
        text = text + await message_quests(query.from_user.id, quests, "daily")

        await query.message.edit_text(
            text=text,
            reply_markup=keyboard
        )

@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.other_quests),
    QuestsCallback.filter(F.action == QuestsAction.skip)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    text = f"🤖: Здесь квесты без ограничения по времени!\n\n"

    if await check_generate_other_quests(query.from_user.id):
        quests = await get_other_quests(query.from_user.id)
    else:
        quests = await generate_other_quests(query.from_user.id)

    text = text + await message_quests(query.from_user.id, quests, "other")

    keyboard = await get_quests_keyboard("other")

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.other_quests),
    QuestsCallback.filter(F.action == QuestsAction.check_execution)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    quests = await get_other_quests(query.from_user.id)
    text = await execution_daily_quests_completed(query.from_user.id, quests, "other")

    await query.answer(text=text, show_alert=True)

    if text != "🤖: Пока нет обновлений!":
        keyboard = await get_quests_keyboard("other")
        text = f"🤖: Подкинул тебе заданий на сегодня!\n\n"
        text = text + await message_quests(query.from_user.id, quests, "other")

        await query.message.edit_text(
            text=text,
            reply_markup=keyboard
        )


@router.callback_query(
    QuestsCallback.filter(F.category == QuestsCategory.main),
    QuestsCallback.filter(F.action == QuestsAction.skip)
)
async def back_main_quests_menu(query: CallbackQuery, callback_data: QuestsCallback, bot: Bot):
    keyboard = await get_main_quests_keyboard()
    text = f"🤖: Выбери какие квесты хочешь посмотреть и не забудь про ежедневный бонус!"

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def execution_daily_quests_completed(tg_id, quests, category_quest):
    update_quests = False
    text = ""

    for counter, quest in enumerate(quests, 1):

        if await check_quest_completed(tg_id, quest["quests_id"], category_quest):

            prize = await get_prize_text(quest)

            type_quest = quest["type_quest"]

            match type_quest:
                case "task":
                    print("task")
                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                    number = str_info[-1]
                    count = int(str_info[2])

                    if number == "номера":
                        number = 0
                    else:
                        number = int(str_info[-1])

                    list_count = await get_daily_temp(tg_id, "task", number)

                    for task in list_count:
                        count_r = task["count_r"]
                        print(count_r, count)
                        if count_r >= count:
                            print("task_completed")
                            await add_points(tg_id, quest["points_quest"])
                            await add_quest_completed(tg_id, quest["quests_id"], "daily")
                            text += (f"🤖: Ты выполнил квест: {quest["title_quests"]}!\n"
                                     f"Получай награду: {prize}\n\n")
                            update_quests = True
                            break

                case "test":
                    print("test")

                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                    number = str_info[5]
                    percent_completion = str_info[-1]

                    if number == "номера":
                        number = 0
                    else:
                        number = int(str_info[5])

                    percent_completion = int(percent_completion[0:2])
                    print(number, percent_completion)

                    list_count = await get_daily_temp(tg_id, "test", number)

                    for task in list_count:
                        count_r = task["count_r"]
                        print(count_r,  percent_completion)
                        if count_r >= percent_completion:
                            print("task_completed")
                            await add_points(tg_id, quest["points_quest"])
                            await add_quest_completed(tg_id, quest["quests_id"], "daily")
                            text += (f"🤖: Ты выполнил квест: {quest["title_quests"]}!\n"
                                     f"Получай награду: {prize}\n\n")
                            update_quests = True
                            break

                case "var":

                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                case "daily_task":

                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                case "every_day":

                    count_quests = 0

                    for j in range(3):
                        quest = quests[j]
                        if not await check_quest_completed(tg_id, quest["quests_id"], "daily"):
                            count_quests += 1
                    print("Выполнено квестов", count_quests)
                    if count_quests == 3:
                        await add_quest_completed(tg_id, quest["quests_id"], "daily")
                        await add_item_in_backpack(tg_id, quest["item_id"], quest["count_item"])

                        text += (f"🤖: Ты выполнил квест: {quest["title_quests"]}!\n"
                                 f"Получай награду: {prize}\n\n")
                        update_quests = True

                case "ref":

                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                    count_invite = str_info[1]
                    count_invite = int(count_invite)

                    print(quest["title_quests"], count_invite)

                    print(quest)

                    if await get_count_invite(tg_id) >= count_invite:
                        await add_quest_completed(tg_id, quest["quests_id"], "other")

                        if quest["type_prize"] == "points":
                            await add_points(tg_id, quest["points_quest"])
                        else:
                            await add_item_in_backpack(tg_id, quest["item_id"], quest["count_item"])

                        if quest["next_quest_id"] is not None:
                            await add_student_quest(tg_id, quest["quests_id"], quest["next_quest_id"])
                        else:
                            await delete_student_quest(tg_id, quest["quests_id"])

                        text += (f"🤖: Ты выполнил квест: {quest["title_quests"]}!\n\n"
                                 f"Получай награду: {prize}")

                        update_quests = True

                case "update_league":
                    str_info = quest["title_quests"]
                    str_info = str_info.split()

                    league_id = str_info[2]
                    league_id = int(league_id)

                    if await get_league_id(tg_id) >= league_id:
                        await add_quest_completed(tg_id, quest["quests_id"], "other")

                        if quest["type_prize"] == "points":
                            await add_points(tg_id, quest["points_quest"])
                        else:
                            await add_item_in_backpack(tg_id, quest["item_id"], quest["count_item"])

                        if quest["next_quest_id"] is not None:
                            await add_student_quest(tg_id, quest["quests_id"], quest["next_quest_id"])
                        else:
                            await delete_student_quest(tg_id, quest["quests_id"])

                        text += (f"🤖: Ты выполнил квест: {quest["title_quests"]}!\n\n"
                                 f"Получай награду: {prize}")

                        update_quests = True

    if update_quests is False:
        text = "🤖: Пока нет обновлений!"
    print(update_quests, text)
    return text


async def message_quests(tg_id, quests, category_quest):
    table_quests = ""

    for counter, quest in enumerate(quests, 1):

        prize = await get_prize_text(quest)

        if await check_quest_completed(tg_id, quest['quests_id'], category_quest):
            table_quests += (f"[{counter}] 🔖 {quest['title_quests']} 🔖\n\n"
                             f"Награда: {prize}\n\n")
        else:
            table_quests += (f"✅ Квест выполнен ✅\n"
                             f"[{counter}] 🔖 {quest['title_quests']} 🔖\n\n"
                             f"Получено: {prize}\n\n")

    return table_quests

async def get_prize_text(quest):
    prize = ""
    if quest["type_prize"] == "points":
        prize = f"🔷 {quest["points_quest"]}"
    elif quest["type_prize"] == "case":
        title_item = await get_title_item(quest["item_id"])
        prize = f"x{quest["count_item"]}🎁 {title_item}"
    elif quest["type_prize"] == "boost":
        title_item = await get_title_item(quest["item_id"])
        prize = f"x{quest["count_item"]}🔷 {title_item}"
    elif quest["type_prize"] == "lottery":
        prize = f"🎟 Участие в ежемесячном розыгрыше"

    return prize