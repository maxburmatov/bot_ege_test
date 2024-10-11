import os

from random import choices, randint, uniform

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from re import findall

from core.database.metods.backpack_student import get_title_item, add_item_in_backpack
from core.database.metods.change_student import add_points, update_collect_daily_bonus
from core.database.metods.check_student import check_collect_daily_bonus
from core.database.metods.get_student import get_count_invite, get_daily_temp, get_days_daily_bonus
from core.database.metods.quests import check_generate_daily_quests, get_daily_quests, generate_daily_quests, \
    check_quest_completed, add_quest_completed
from core.keyboards.inline_quests import get_main_quests_keyboard, QuestsCallback, QuestsCategory, QuestsAction, \
    get_daily_quests_keyboard, get_daily_bonus_keyboard
from core.lexicon.lexicon import LEXICON_BUTTON


router = Router()


@router.message(F.text == LEXICON_BUTTON["quests"])
async def backpack_page_handler(message: Message,  bot: Bot):
    keyboard = await get_main_quests_keyboard()  # Page: 0
    text = f"🤖: Выбери какие квесты хочешь посмотреть и не забудь про ежедневный бонус!"

    await bot.send_message(
        text=text ,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )
    await message.delete()

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
        daily_bonus = daily_bonus_by_day[f"{str(days_in_row+1)}"]
        text = (f"🤖: Ежедневный бонус собран!\n\n"
                f"Тебе начислено: 🔷 {daily_bonus}!")
        await update_collect_daily_bonus(query.from_user.id)
        await add_points(query.from_user.id, daily_bonus)

        text_change = await message_daily_bonus(days_in_row+1, daily_bonus_by_day)
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

    text = text + await message_daily_quests(query.from_user.id, quests)

    keyboard = await get_daily_quests_keyboard()

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
    text = await execution_daily_quests_completed(query.from_user.id, quests)

    await query.answer(text=text, show_alert=True)

    if text != "🤖: Пока нет обновлений!":
        keyboard = await get_daily_quests_keyboard()
        text = f"🤖: Подкинул тебе заданий на сегодня!\n\n"
        text = text + await message_daily_quests(query.from_user.id, quests)

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

async def execution_daily_quests_completed(tg_id, quests):

    update_quests = False
    text = ""

    for counter, quest in enumerate(quests, 1):

        if await check_quest_completed(tg_id, quest[0]):

            prize = ""

            if quest[3] == "points":
                prize = f"🔷 {quest[4]}"
            elif quest[3] == "case":
                title_item = await get_title_item(quest[5])
                prize = f"🎁 {title_item}"

            category_quest = quest[2]

            match category_quest:
                case "ref":

                    if await get_count_invite(tg_id) != 0:
                        await add_points(tg_id, quest[3])
                        await add_quest_completed(tg_id, quest[0])
                        text += (f"🤖: Ты выполнил квест: {quest[1]}!\n"
                                f"Получай награду: {prize}\n\n")
                        update_quests = True

                case "task":
                    print("task")
                    str_info = quest[1]
                    str_info = str_info.split()

                    number = int(str_info[-1])
                    count = int(str_info[1])
                    count_all, count_r = await get_daily_temp(tg_id, "task", number)
                    if count_all >= count:
                        print("task_completed")
                        await add_points(tg_id, quest[4])
                        await add_quest_completed(tg_id, quest[0])
                        text += (f"🤖: Ты выполнил квест: {quest[1]}!\n"
                                f"Получай награду: {prize}\n\n")
                        update_quests = True

                case "test":
                    print("test")

                    str_info = quest[1]
                    str_info = str_info.split()

                    number = int(str_info[-1])
                    count = int(str_info[1])
                    count_all, count_r = await get_daily_temp(tg_id, "test", number)
                    if count_all >= count:
                        print("test_completed")
                        await add_points(tg_id, quest[4])
                        await add_quest_completed(tg_id, quest[0])
                        text += (f"🤖: Ты выполнил квест: {quest[1]}!\n"
                                f"Получай награду: {prize}\n\n")
                        update_quests = True

                case "var":

                    str_info = quest[1]
                    str_info = str_info.split()

                case "every_day":

                    count_quests = 0

                    for j in range(3):
                        if not await check_quest_completed(tg_id, quest[0]):
                            count_quests += 1

                    if count_quests == 3:
                        await add_quest_completed(tg_id, quest[0])
                        await add_item_in_backpack(tg_id, quest[5], 1)

                        text += (f"🤖: Ты выполнил квест: {quest[1]}!\n"
                                f"Получай награду: {prize}\n\n")
                        update_quests = True

    if update_quests is False:
        text = "🤖: Пока нет обновлений!"
    print(update_quests, text)
    return text

async def message_daily_quests(tg_id, quests):
    table_quests = ""
    prize = ""
    for counter, quest in enumerate(quests, 1):
        if quest[3] == "points":
            prize = f"🔷 {quest[4]}"
        elif quest[3] == "case":
            title_item = await get_title_item(quest[5])
            prize = f"🎁 {title_item}"

        if await check_quest_completed(tg_id, quest[0]):
            table_quests += (f"[{counter}] 🔖 {quest[1]} 🔖\n\n"
                            f"Награда: {prize}\n\n")
        else:
            table_quests += (f"✅ Квест выполнен ✅\n"
                            f"[{counter}] 🔖 {quest[1]} 🔖\n\n"
                            f"Получено: {prize}\n\n")

    return table_quests





