import os

from random import choices, randint, uniform

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from core.database.metods.change_student import change_avatar, add_points, update_use_boost
from core.database.metods.backpack_student import get_backpack_items, get_info_case, get_image_open_case, \
    add_item_in_backpack, delete_item_in_backpack
from core.database.metods.check_student import check_use_boost
from core.database.metods.get_student import get_remaining_time_boost
from core.keyboards.inline_backpack import BackpackCallback, BackpackCategory, BackpackAction, \
    get_avatars_backpack_keyboard, get_cases_backpack_keyboard, get_other_backpack_keyboard, get_main_backpack_keyboard

from re import findall

from core.keyboards.reply import back_menu, open_case_menu
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_MEDIA, LEXICON_STICKERS
from core.services.create_image import create_prize_image
from core.utils.functions import delete_message

router = Router(name=__name__)

@router.message((F.text == LEXICON_BUTTON["my_backpack"]) | (F.text == "/backpack"))
async def backpack_page_handler(message: Message,  bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(
        "🤖: В рюкзаке хранятся твои предметы!",
        reply_markup=back_menu)
    keyboard = await get_main_backpack_keyboard()  # Page: 0
    path = LEXICON_MEDIA["my_backpack"]
    image = FSInputFile(path)
    caption = f"🤖: Выбери нужную категорию!"

    await bot.send_photo(
        photo=image,
        caption=caption,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )

@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.avatars),
    BackpackCallback.filter(F.action == BackpackAction.skip)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    page = int(callback_data.page)
    info_items, count_items = await check_items(query.from_user.id, "avatar")

    keyboard = await get_avatars_backpack_keyboard(page, count_items)
    item = info_items[page]
    caption = f"[{item['title_item']}] x{item['count_item']}"
    photo = InputMediaPhoto(media=item['image_backpack'], caption=caption)

    await query.message.edit_media(photo, reply_markup=keyboard)


@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.avatars),
    BackpackCallback.filter(F.action == BackpackAction.change_avatar)
    )
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    page = int(callback_data.page)
    info_items, count_items = await check_items(query.from_user.id, "avatar")
    item = info_items[page]

    await change_avatar(query.from_user.id, item['item_id'])
    await query.answer(f"Аватар изменен на {item['title_item']}!")


@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.cases),
    BackpackCallback.filter(F.action == BackpackAction.skip)
    )
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    page = int(callback_data.page)
    info_items, count_items = await check_items(query.from_user.id, "case")

    if count_items != 0:
        item = info_items[page]
        keyboard = await get_cases_backpack_keyboard(page, count_items)
        caption = f"[{item['title_item']}] x{item['count_item']}"
        photo = InputMediaPhoto(media=item['image_backpack'], caption=caption)

        await query.message.edit_media(photo, reply_markup=keyboard)
    else:
        await query.answer("У тебя пока нет кейсов!")

@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.cases),
    BackpackCallback.filter(F.action == BackpackAction.open_case)
    )
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    await bot.delete_message(query.from_user.id, query.message.message_id)

    page = int(callback_data.page)
    info_items, count_items = await check_items(query.from_user.id, "case")

    if count_items != 0:
        item = info_items[page]
        item_id = item['item_id']

        await bot.send_sticker(query.from_user.id, LEXICON_STICKERS["open_case"])

        prize = await generation_prize_from_case(item_id)
        image_prize = await create_prize_image(item_id, prize)
        image = FSInputFile(image_prize)
        text_prize = await add_prize(query.from_user.id, prize)
        await delete_item_in_backpack(query.from_user.id, item_id)

        await bot.send_photo(query.from_user.id, image)
        os.remove(image_prize)

        await bot.send_message(query.from_user.id, text_prize, reply_markup=open_case_menu)
    else:
        await bot.send_message(query.from_user.id, f"🤖: У тебя закончились эти кейсы!")


@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.other),
    BackpackCallback.filter(F.action == BackpackAction.skip)
    )
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    page = int(callback_data.page)
    info_items, count_items = await check_items(query.from_user.id, "boost")

    if count_items != 0:
        item = info_items[page]
        keyboard = await get_other_backpack_keyboard(page, count_items)
        caption = f"[{item['title_item']}] x{item['count_item']}"
        photo = InputMediaPhoto(media=item['image_backpack'], caption=caption)

        await query.message.edit_media(photo, reply_markup=keyboard)
    else:
        await query.answer("У тебя пока нет предметов!")


@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.other),
    BackpackCallback.filter(F.action == BackpackAction.use_boost)
    )
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    page = int(callback_data.page)

    if await check_use_boost(query.from_user.id):
        text_hours = await get_remaining_time_boost(query.from_user.id)
        await query.answer(f"🤖: Ты уже используешь множитель опыта! Он будет активен еще {text_hours}!")
    else:
        info_items, count_items = await check_items(query.from_user.id, "boost")
        item = info_items[page]
        item_id = item['item_id']
        time_boost, time_answer = await definition_time_boost(item)
        await update_use_boost(query.from_user.id, time_boost)
        await delete_item_in_backpack(query.from_user.id, item_id)
        await query.answer(f"🤖: Множитель опыта активирован на {time_answer}!")

@router.callback_query(
    BackpackCallback.filter(F.category == BackpackCategory.main),
    BackpackCallback.filter(F.action == BackpackAction.skip)
)
async def backpack_page_handler(query: CallbackQuery, callback_data: BackpackCallback, bot: Bot):
    keyboard = await get_main_backpack_keyboard()  # Page: 0
    path = LEXICON_MEDIA["my_backpack"]
    path = FSInputFile(path)

    caption = f"🤖: В рюкзаке хранятся твои предметы!"

    photo = InputMediaPhoto(media=path, caption=caption)

    await query.message.edit_media(photo, reply_markup=keyboard)

@router.callback_query(F.data == "dont_click_me!")
async def backpack_page_handler(query: CallbackQuery, bot: Bot):
    await query.answer()

async def check_items(tg_id, type_item):
    info_items = await get_backpack_items(tg_id, type_item)
    count_items = len(info_items)
    return info_items, count_items

async def generation_prize_from_case(item_id):
    info_case = await get_info_case(item_id)
    number_items = [i for i in range(0, len(info_case))]
    weights_items = [info_case[i]['weight_item'] for i in range(0, len(info_case))]

    number = choices(number_items, weights=weights_items, k=1)[0]

    prize = info_case[number]

    return prize

async def add_prize(tg_id, prize):

    text = ""
    type_item = prize['type_item']

    if type_item == "avatar":
        text = f"🤖: Закинул автар профиля в твой рюкзак!"
        await add_item_in_backpack(tg_id, prize['item_id'], 1)
    elif type_item == "boost":
        text = f"🤖: Закинул множитель баллов в твой рюкзак!"
        await add_item_in_backpack(tg_id, prize['item_id'], 1)
    elif type_item == "points":
        range_points = findall(r'\d+', prize['title_item'])
        range_points = [int(i) for i in range_points]
        random_points = randint(range_points[0], range_points[1])
        text = f"🤖: Тебе начислено 🔷 {random_points}!"
        await add_points(tg_id, random_points)
    elif type_item == "usdt":
        range_usdt = findall(r'\d*\.\d+|\d+', prize['title_item'])
        range_usdt = [float(i) for i in range_usdt]
        random_usdt = uniform(range_usdt[0], range_usdt[1])
        random_usdt = round(random_usdt, 2)
        text = f"🤖: Тебе начислено 💵 {random_usdt} USDT!"

    return text

async def definition_time_boost(item):
    title_item = item['title_item']
    title_item = title_item.split(" ")
    time_boost = int(title_item[4])

    time_answer = ""
    if time_boost == 12:
        time_answer = f"12 часов"
    elif time_boost == 24:
        time_answer = f"24 часа"

    return time_boost, time_answer