import sqlite3

from datetime import datetime

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

daily_bonus_by_day = {"1": 5, "2": 10, "3": 18, "4": 30, "5": 50, "6": 75, "7": 100}

async def get_name(tg_id):
    cur.execute(f'SELECT name FROM students WHERE tg_id = {tg_id}')
    info = cur.fetchone()
    name = info[0]
    return name

async def get_league_id(tg_id):
    cur.execute(f'SELECT league_id FROM students WHERE tg_id = {tg_id}')
    info = cur.fetchone()
    name = info[0]
    return name

async def get_remaining_time_boost(tg_id):
    data = await get_time_end_boost(tg_id)
    data_end = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
    data_now = datetime.now()

    if data_now < data_end:
        time_dif = data_end - data_now
        dif_sec = time_dif.seconds
        dif_hours = int(round(dif_sec / 3600, 0))

        match dif_hours:
            case 0:
                text_hours = "менее часа"
            case 1 | 21:
                text_hours = f"{dif_hours} час"
            case 2 | 3 | 4 | 22 | 23 | 24:
                text_hours = f"{dif_hours} часа"
            case _:
                text_hours = f"{dif_hours} часов"
    else:
        cur.execute(f'UPDATE students SET boost = NULL WHERE tg_id = {tg_id}')
        conn.commit()
        text_hours = "Неактивен"

    return text_hours

async def get_time_end_boost(tg_id):
    cur.execute(
        f'SELECT boost FROM students WHERE tg_id = {tg_id}')
    data = cur.fetchone()
    data = data[0]

    return data

async def get_info_student(tg_id):

    info_student = {}

    cur.execute(
        f'SELECT name, purpose_id, points, league_id, avatar_id, stars, boost FROM students WHERE tg_id = {tg_id}')

    stats = cur.fetchone()
    name = stats[0]
    purpose = stats[1]
    points = stats[2]
    league_id = stats[3]
    avatar_id = stats[4]
    stars = stats[5]
    boost = stats[6]

    if purpose == 1:
        purpose = "до 70"
    elif purpose == 2:
        purpose = "70-85"
    elif purpose == 3:
        purpose = "85-95"
    elif purpose == 4:
        purpose = "95+"

    if boost is not None:
        time_boost = await get_remaining_time_boost(tg_id)
    else:
        time_boost = "Неактивен"

    info_student["name"] = name
    info_student["purpose"] = purpose
    info_student["points"] = points
    info_student["league_id"] = league_id
    info_student["avatar_id"] = avatar_id
    info_student["stars"] = stars
    info_student["time_boost"] = time_boost

    return info_student

async def get_count_invite(tg_id):
    cur.execute(f'SELECT COUNT(*) FROM students WHERE invited_tg_id = {tg_id}')
    info = cur.fetchone()
    count = info[0]
    return count

async def get_daily_temp(tg_id, action, number):
    if number == 0:
        cur.execute(
            f'SELECT count_all, count_r FROM students_daily_temp WHERE tg_id = {tg_id} and action = "{action}"')
        data = cur.fetchall()
    else:
        cur.execute(
            f'SELECT count_all, count_r FROM students_daily_temp WHERE tg_id = {tg_id} and action = "{action}" and number = {number}')
        data = cur.fetchall()

    list_count = []

    if not data:
        dict_count = {"count_all": 0, "count_r": 0}
        list_count.append(dict_count)
    else:
        for temp in data:
            dict_count = {"count_all": temp[0], "count_r": temp[1]}
            list_count.append(dict_count)
    print(list_count)
    return list_count

async def get_days_daily_bonus(user_id):
    cur.execute(f'SELECT days_in_row FROM students WHERE tg_id = {user_id}')
    info = cur.fetchone()
    days_in_row = info[0]

    return days_in_row, daily_bonus_by_day





