import os

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile

from core.database.metods.table_leaders import get_info_table_leaders
from core.keyboards.reply import main_menu
from core.lexicon.endings_words import ending_hours
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.services.create_image import create_table_leaders_image
from core.utils.functions import get_hours_update_league

router = Router()

@router.message(F.text == LEXICON_BUTTON["table_leaders"])
async def my_room(message: Message, bot: Bot):
    await message.delete()
    await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["transfer"])

    info_all_students, current_student, prize_league = await get_info_table_leaders(message.from_user.id)
    hours_update_league = await get_hours_update_league()
    league_id = current_student['league_id']
    league_title = current_student['title_league']
    count_students_league = current_student['count_students']
    place = current_student['place']
    points = current_student['points']

    path = await create_table_leaders_image(info_all_students, current_student['league_id'], prize_league)
    image = FSInputFile(path)
    await message.answer_photo(image)
    os.remove(path)

    league_answer, place_answer, stars_answer = await message_league_info(league_id, league_title, place, points, count_students_league)

    await message.answer(f"{league_answer}")
    await message.answer(f"{place_answer}")
    await message.answer(f"{stars_answer}")
    await message.answer(
        f"🤖: Чем выше лига, тем круче подарки! Дойдя до последней лиги ты получишь подарки в конце месяца, а первые 10 человек примут участие в розыгрыше!")
    await message.answer(
        f"🤖: До обновления лиг: {hours_update_league} {await ending_hours(hours_update_league)}!",
        reply_markup=main_menu)

async def message_league_info(league_id, league_title, place, points, count_students_league):
    match league_id:
        case 4:
            league_answer = f'🤖: Сейчас ты в последней лиге: {league_title}. Твоя задача войти в ТОП-10 до конца месяца чтобы получить награды!'
            match place:
                case 1:
                    place_answer = f"🤖: Ты лидер в своей лиге! Твое место: {place}. У тебя: 🔷 {points} баллов. В конце месяца ты получишь подарочки и примешь участие в розыгрыше! Докажи свое превосходство!"
                case 2:
                    place_answer = f"🤖: Ты дышишь в спину лидеру! Твое место: {place}. У тебя: 🔷 {points} баллов. В конце месяца ты получишь подарочки и примешь участие в розыгрыше! Сможешь перегнать лидера?"
                case 3:
                    place_answer = f"🤖: Ты уже в ТОП-3! Твое место: {place}. У тебя: 🔷 {points} баллов. В конце месяца ты получишь подарочки и примешь участие в розыгрыше! У тебя есть все шансы стать лидером в этой лиге!"
                case _:
                    if place <= 10:
                        place_answer = f"🤖: Твое место: {place}. У тебя: 🔷 {points} баллов. В конце месяца ты получишь подарочки и примешь участие в розыгрыше! Постарайся не потерять своё место, а еще лучше подняться выше!"
                    else:
                        place_answer = f"🤖: Твое место: {place}. У тебя: 🔷 {points} баллов. В конце месяца ты получишь подарочки, но чтобы принять участие в розыгрыше тебе нужно занять хотя бы 10 место!"
        case _:
            league_answer = f'🤖: Сейчас ты в лиге: {league_title}. Каждые 3 дня происходит обновление лиг. В следующую лигу проходят первые {count_students_league} человек!'
            match place:
                case 1:
                    place_answer = f"🤖: Ты лидер в своей лиге! Твое место: {place}. У тебя: 🔷 {points} баллов. На данный момент ты проходишь в следующую лигу. Докажи свое превосходство!"
                case 2:
                    place_answer = f"🤖: Ты дышишь в спину лидеру! Твое место: {place}. У тебя: 🔷 {points} баллов. На данный момент ты проходишь в следующую лигу. Сможешь перегнать лидера?"
                case 3:
                    place_answer = f"🤖: Ты уже в ТОП-3! Твое место: {place}. У тебя: 🔷 {points} баллов. На данный момент ты проходишь в следующую лигу. У тебя есть все шансы стать лидером в этой лиге!"
                case _:
                    if place <= count_students_league:
                        place_answer = f"🤖: Твое место: {place}. У тебя: 🔷 {points} баллов. На данный момент ты проходишь в следующую лигу. Постарайся не потерять своё место, а еще лучше подняться выше!"
                    else:
                        place_answer = f"🤖: Твое место: {place}. У тебя: 🔷 {points} баллов. На данный момент ты не проходишь в следующую лигу. Тебе нужно занять хотя бы {count_students_league} место!"

    if league_id == 1:
        stars_answer = f"🤖: Также есть особая валюта - звезды лидера. На них можно купить уникальные предметы в магазине! Чтобы их получить нужно войти в ТОП-3 в следующих лигах!"
    else:
        stars_answer = f"🤖: Первые 3 человека получат особую валюту - звезды лидера. На них можно купить уникальные предметы в магазине!"

    return league_answer, place_answer, stars_answer