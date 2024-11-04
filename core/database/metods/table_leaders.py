import sqlite3

from datetime import datetime

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_info_table_leaders(tg_id):
    current_student = await get_info_student_league(tg_id)
    all_students = await get_table_top10(current_student['league_id'])
    prize_league = await get_prize_league(current_student['league_id'])
    return all_students, current_student, prize_league

async def get_info_student_league(tg_id):
    info_student = {}
    cur.execute(
        f'SELECT league_id, title_league, count_students FROM students JOIN league ON league_id = league.id WHERE tg_id = {tg_id}')
    stats = cur.fetchone()

    info_student["league_id"] = stats[0]
    info_student["title_league"] = stats[1]
    info_student["count_students"] = stats[2]

    cur.execute(
        f'SELECT name, points, image_item, RowNumber FROM (SELECT tg_id, name, points, avatar_id, ROW_NUMBER() OVER(ORDER BY points DESC) AS RowNumber '
        f'FROM students WHERE league_id = {info_student['league_id']}) '
        f'JOIN items_all ON id = avatar_id WHERE tg_id = {tg_id} ')

    current_student = cur.fetchone()

    avatar_title = current_student[2]
    avatar_image = f"./core/media/table_leaders/avatars/{avatar_title}"
    image_item = avatar_image

    info_student["name"] = current_student[0]
    info_student["points"] = current_student[1]
    info_student["avatar_image"] = image_item
    info_student["place"] = current_student[3]

    return info_student


async def get_table_top10(league_id):
    cur.execute(
        f'SELECT name, points, image_item FROM students JOIN items_all ON id = avatar_id WHERE league_id = {league_id} order by points desc limit 10')
    data = cur.fetchall()

    all_students = []
    for student in data:
        list_student = list(student)
        avatar_title = student[2]
        avatar_image = f"./core/media/table_leaders/avatars/{avatar_title}"
        list_student[2] = avatar_image
        all_students.append(list_student)

    return all_students


async def get_prize_league(league_id):
    cur.execute(
        f'SELECT place, prize_points, image_item, count_item, stars FROM league_prize JOIN items_all ON item_id = items_all.id WHERE league_id = {league_id}')
    data = cur.fetchall()

    info_prize_with_items = []
    for item in data:
        list_item = list(item)
        item_title = item[2]
        item_image = f"./core/media/table_leaders/items/{item_title}"
        list_item[2] = item_image
        info_prize_with_items.append(list_item)

    cur.execute(
        f'SELECT place, prize_points FROM league_prize WHERE league_id = {league_id} and item_id = 0')
    info_prize_without_items = cur.fetchall()

    prize_league = info_prize_with_items + info_prize_without_items

    return prize_league

async def get_table_leaders(league_id):
    cur.execute(
        f'SELECT count_students FROM league WHERE id = {league_id}')
    info_league = cur.fetchone()
    count_students = info_league[0]

    cur.execute(f'SELECT tg_id, ROW_NUMBER() OVER(ORDER BY points DESC) AS place_student, points, name FROM students WHERE students.league_id = {league_id} LIMIT {count_students}')
    table_leaders = cur.fetchall()

    cur.execute(
        f'SELECT place, prize_points, item_id, count_item, stars, title_item FROM league_prize JOIN items_all ON item_id = items_all.id WHERE league_id = {league_id}')
    table_prize = cur.fetchall()

    cur.execute(
        f'SELECT place, prize_points FROM league_prize WHERE league_id = {league_id} and item_id = 0')
    table_prize1 = cur.fetchall()

    table_all_prize = table_prize + table_prize1
    print(table_all_prize)

    return table_leaders, table_all_prize
