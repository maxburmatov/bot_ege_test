import sqlite3

from datetime import datetime, timedelta

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def change_avatar(tg_id, avatar_id):
    cur.execute(
        f'UPDATE students SET avatar_id = {avatar_id} WHERE tg_id = {tg_id}')
    conn.commit()

async def change_name(tg_id, new_name):
    cur.execute(f'UPDATE students SET name = "{new_name}" WHERE tg_id = {tg_id}')
    conn.commit()


async def add_points(tg_id, points):
    print(f"Начислено: {points}")
    cur.execute(f'UPDATE students SET points = points + {points} WHERE tg_id = {tg_id}')
    conn.commit()


async def update_use_boost(tg_id, time_boost):
    data = ''
    if time_boost == 12:
        data = datetime.now() + timedelta(hours=12)
    elif time_boost == 24:
        data = datetime.now() + timedelta(days=1)

    cur.execute(f'UPDATE students SET boost = "{data}" WHERE tg_id = {tg_id}')
    conn.commit()


async def reset_use_boost(tg_id):
    cur.execute(f'UPDATE students SET boost = NULL WHERE tg_id = {tg_id}')
    conn.commit()

async def update_collect_daily_bonus(tg_id):
    cur.execute(f'UPDATE students_daily SET collect_daily_points = 1 WHERE tg_id = {tg_id}')
    cur.execute(f'UPDATE students SET days_in_row = days_in_row + 1 WHERE tg_id = {tg_id}')
    conn.commit()


async def add_task(tg_id):
    cur.execute(f'UPDATE general_stats_students SET tasks = tasks + 1 WHERE tg_id = {tg_id}')
    cur.execute(f'UPDATE students_daily SET tasks = tasks + 1 WHERE tg_id = {tg_id}')
    conn.commit()

async def add_test(tg_id):
    cur.execute(f'UPDATE general_stats_students SET tests = tests + 1 WHERE tg_id = {tg_id}')
    cur.execute(f'UPDATE students_daily SET tests = tests + 1 WHERE tg_id = {tg_id}')
    conn.commit()

async def add_time_tasks(tg_id, tasks_time):
    cur.execute(f'UPDATE general_stats_students SET tasks_time = tasks_time + {tasks_time} WHERE tg_id = {tg_id}')
    conn.commit()

async def students_upgrade_league(tg_id, league_id):
    cur.execute(f'UPDATE students SET league_id = league_id + 1 WHERE tg_id = {tg_id} and league_id = {league_id}')
    conn.commit()
    print("Лига обновлена")

async def add_stars(user_id, stars):
    cur.execute(f'UPDATE students SET stars = stars + {stars} WHERE tg_id = {user_id}')
    conn.commit()

