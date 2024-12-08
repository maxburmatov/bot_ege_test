from random import randint
from prettytable import PrettyTable

from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.metods.admin_metods import get_general_info_bots, get_info_all_bots, admin_add_points, admin_del_points, admin_change_name, \
    admin_change_avatar, admin_add_bot
from core.filters.user_filters import IsAdmin

from core.keyboards.reply_admin import admin_bots_menu
from core.lexicon.lexicon import LEXICON_BUTTON
from core.states.states import StateAdminAddPointsAllBots
from core.utils.functions import delete_message

router = Router()


@router.message(F.text == LEXICON_BUTTON["admin_bots"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    bots_dict = await get_general_info_bots()

    bots_info = (f"Кол-во ботов: {bots_dict["count_bots"]}\n\n"
                 f"Новички: {bots_dict["count_bots_league_1"]}\n"
                 f"Опытные: {bots_dict["count_bots_league_2"]}\n"
                 f"Профи: {bots_dict["count_bots_league_3"]}\n"
                 f"Сверхразумы: {bots_dict["count_bots_league_4"]}\n"
                 )

    table = await generate_table()

    await message.answer(bots_info, reply_markup=admin_bots_menu)

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text == LEXICON_BUTTON["all_bots_add_points"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Напиши диапазон начисляемых баллов (формат: 1-20)", reply_markup=admin_bots_menu)

    await state.set_state(StateAdminAddPointsAllBots.ADD_POINTS)

@router.message(StateFilter(StateAdminAddPointsAllBots.ADD_POINTS), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text
    text.split("-")
    points_a = int(text[0])
    points_b = int(text[-1])

    await add_points_all_bots(points_a, points_b)

    table = await generate_table()

    await message.answer(f"🤖: Баллы успешно начислены!", reply_markup=admin_bots_menu)

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await state.clear()

@router.message(F.text == LEXICON_BUTTON["bot_edit"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    table = await generate_table()

    text_info = ("Список действий:\n\n"
                 "Добавить баллы - <code>/add_points</code>\n"
                 "Снять баллы - <code>/del_points</code>\n"
                 "Изменить имя - <code>/change_name</code>\n"
                 "Изменить аватар - <code>/change_avatar</code>\n"
                 "Формат запроса: /команда tg_id значение"
                 )

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: {text_info}", reply_markup=admin_bots_menu, parse_mode=ParseMode.HTML)

@router.message(F.text == LEXICON_BUTTON["bot_add"], IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    table = await generate_table()

    text_info = ("Список действий:\n\n"
                 "Добавить бота - <code>/add_bot</code>\n"
                 "Формат запроса: /команда tg_id имя баллы avatar_id league_id"
                 )

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: {text_info}", reply_markup=admin_bots_menu, parse_mode=ParseMode.HTML)

@router.message(F.text.startswith('/add_bot'), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text

    text = text.split(" ")
    tg_id = int(text[1])
    name = text[2]
    points = int(text[3])
    avatar_id = int(text[4])
    league_id = int(text[5])

    await admin_add_bot(tg_id, name, points, avatar_id, league_id)
    table = await generate_table()

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: tg_id: {tg_id}, имя: {name}, баллы: {points}, avatar_id: {avatar_id}, league_id: {league_id}", reply_markup=admin_bots_menu)

@router.message(F.text.startswith('/add_points'), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text

    text = text.split(" ")
    tg_id = int(text[1])
    points = int(text[2])

    await admin_add_points(tg_id, points)
    table = await generate_table()

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: tg_id: {tg_id}, добавлено: {points}", reply_markup=admin_bots_menu)

@router.message(F.text.startswith('/del_points'), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text

    text = text.split(" ")
    tg_id = int(text[1])
    points = int(text[2])

    await admin_del_points(tg_id, points)
    table = await generate_table()

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: tg_id: {tg_id}, снято: {points}", reply_markup=admin_bots_menu)

@router.message(F.text.startswith('/change_name'), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text

    text = text.split(" ")
    tg_id = int(text[1])
    name = text[2]

    await admin_change_name(tg_id, name)
    table = await generate_table()

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: tg_id: {tg_id}, новое имя: {name}", reply_markup=admin_bots_menu)

@router.message(F.text.startswith('/change_avatar'), IsAdmin())
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text = message.text

    text = text.split(" ")
    tg_id = int(text[1])
    avatar_id = int(text[2])

    await admin_change_avatar(tg_id, avatar_id)
    table = await generate_table()

    await message.answer(f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    await message.answer(f"🤖: tg_id: {tg_id}, новый аватар: {avatar_id}", reply_markup=admin_bots_menu)


async def add_points_all_bots(points_a, points_b):
    bots_list = await get_info_all_bots()

    for bot in bots_list:
        random_points = randint(points_a, points_b)
        await admin_add_points(bot["tg_id"], random_points)

async def generate_table():
    bots_list = await get_info_all_bots()

    table = PrettyTable(['tg_id', 'name', 'points', 'league_id', 'avatar_id'])
    table.align['tg_id'] = 'l'
    table.align['name'] = 'r'
    table.align['points'] = 'r'
    table.align['league_id'] = 'r'
    table.align['avatar_id'] = 'r'

    data = []
    for bot in bots_list:
        bot_tuple = (bot["tg_id"], bot["name"], bot["points"], bot["league_id"], bot["avatar_id"])
        data.append(bot_tuple)

    for tg_id, name, points, league_id, avatar_id in data:
        table.add_row([tg_id, name, points, league_id, avatar_id])

    return table