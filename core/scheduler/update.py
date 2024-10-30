from aiogram import Bot
from core.config_data.config import config
from core.database.metods.backpack_student import add_item_in_backpack
from core.database.metods.change_student import students_upgrade_league, add_points, add_stars
from core.database.metods.table_leaders import get_table_leaders
from core.utils.functions import check_date_update_league

bt = Bot(token=config.bots.bot_token)
async def update_league(bot: Bot):
    if await check_date_update_league():
        table_leaders_league_1, table_prize1 = await get_table_leaders(1)
        table_leaders_league_2, table_prize2 = await get_table_leaders(2)
        table_leaders_league_3, table_prize3 = await get_table_leaders(3)

        '''1 ЛИГА - НОВИЧКИ (ПЕРЕХОД В ОПЫТНЫЕ)'''
        for counter, student in enumerate(table_leaders_league_1):
            student_place = student[1]
            student_id = student[0]

            if student_place <= 3:
                prize_points = table_prize1[counter][1]
            else:
                prize_points = table_prize1[3][1]

            await add_points(student_id, prize_points)
            await students_upgrade_league(student_id, 1)

            await bt.send_message(678723641, text="🤖: Ура! Ты перешел в следующую лигу! Проверь раздел -> 🏆 Рейтинг.")
            await bt.send_message(678723641, text=f"🤖: Тебе начислено: 🔷 {prize_points} ")

        '''2 ЛИГА - ОПЫТНЫЕ (ПЕРЕХОД В ПРОФИ)'''
        for counter, student in enumerate(table_leaders_league_2):
            student_place = student[1]
            student_id = student[0]

            if student_place <= 3:
                item_id = table_prize2[counter][2]
                count_item = table_prize2[counter][3]
                prize_points = table_prize2[counter][1]
                title_item = table_prize2[counter][5]
                stars = table_prize2[counter][4]

                if stars == 1:
                    text_stars = "звезда"
                else:
                    text_stars = "звезды"

                points_answer = f"🤖: Тебе начислено: 🔷 {prize_points} и {stars} {text_stars} лидера!"
                prize_answer = f"🤖: А также закинул в твой инвентарь: x{count_item} 🎁 {title_item}!"
                await add_stars(student_id, stars)
                await add_item_in_backpack(student_id, item_id, count_item)
            else:
                prize_points = table_prize2[3][1]
                prize_answer = f"🤖: Залетай в ТОП-3 чтобы получать дополнительные подарки и звезды лидера!"
                points_answer = f"🤖: Тебе начислено: 🔷 {prize_points}!"

            await add_points(student_id, prize_points)
            await students_upgrade_league(student_id, 2)

            await bt.send_message(chat_id=678723641,text="🤖: Ура! Ты перешел в следующую лигу! Проверь раздел -> 🏆 Рейтинг.")
            await bt.send_message(chat_id=678723641, text=points_answer)
            await bt.send_message(chat_id=678723641, text=prize_answer)

        '''3 ЛИГА - ПРОФИ (ПЕРЕХОД В СВЕРХРАЗУМЫ)'''
        for counter, student in enumerate(table_leaders_league_3):
            student_place = student[1]
            student_id = student[0]

            if student_place <= 3:
                item_id = table_prize2[counter][2]
                count_item = table_prize2[counter][3]
                prize_points = table_prize2[counter][1]
                title_item = table_prize2[counter][5]
                stars = table_prize2[counter][4]

                if stars == 1:
                    text_stars = "звезда"
                else:
                    text_stars = "звезды"

                points_answer = f"🤖: Тебе начислено: 🔷 {prize_points} и {stars} {text_stars} лидера!"
                prize_answer = f"🤖: А также закинул в твой инвентарь: x{count_item} 🎁 {title_item}!"
                await add_stars(student_id, stars)
                await add_item_in_backpack(student_id, item_id, count_item)
            else:
                prize_points = table_prize2[3][1]
                prize_answer = f"🤖: Залетай в ТОП-3 чтобы получать дополнительные подарки и звезды лидера!"
                points_answer = f"🤖: Тебе начислено: 🔷 {prize_points}!"

            await add_points(student_id, prize_points)
            await students_upgrade_league(student_id, 3)

            await bt.send_message(678723641,
                                   text="🤖: Ура! Ты перешел в следующую лигу! Проверь раздел -> 🏆 Рейтинг.")
            await bt.send_message(678723641, text=points_answer)
            await bt.send_message(678723641, text=prize_answer)
    else:
        print("Нет обновления лиг!")
