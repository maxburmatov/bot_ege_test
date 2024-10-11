import sqlite3

from datetime import datetime, timedelta

from core.database.metods.change_student import reset_use_boost
from core.database.metods.get_student import get_time_end_boost

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

limits_no_sub = {"tasks": 20, "tests": 2, "var": 1, "weekly_var": 0}
limits_sub = {"tasks": 40, "tests": 4, "var": 2, "weekly_var": 1}

async def check_use_boost(tg_id):
    data = await get_time_end_boost(tg_id)

    if data is None:
        return False
    else:
        data_end = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
        data_now = datetime.now()
        if data_now < data_end:
            return True
        else:
            await reset_use_boost(tg_id)
            return False

async def check_collect_daily_bonus(tg_id):
    cur.execute(f'SELECT collect_daily_points FROM students_daily WHERE tg_id = {tg_id}')
    info = cur.fetchone()
    col_daily_bonus = info[0]

    if col_daily_bonus == 0:
        return False
    else:
        return True

async def check_daily_tasks(tg_id):
    cur.execute(f'SELECT tasks FROM students_daily WHERE tg_id = {tg_id}')
    info = cur.fetchone()
    tasks = info[0]
    cur.execute(f'SELECT is_sub FROM sub WHERE tg_id = {tg_id}')
    info_sub = cur.fetchone()
    is_sub = info_sub[0]
    if tasks == limits_no_sub["tasks"] and is_sub == 0:
        return False
    elif tasks == limits_sub["tasks"] and is_sub == 1:
        return False
    else:
        return True

async def check_daily_test(tg_id):
    cur.execute(f'SELECT tests FROM students_daily WHERE tg_id = {tg_id}')
    info = cur.fetchone()
    tests = info[0]
    cur.execute(f'SELECT is_sub FROM sub WHERE tg_id = {tg_id}')
    info_sub = cur.fetchone()
    if tests == limits_no_sub["tests"] and info_sub[0] == 0:
        return False
    elif tests == limits_sub["tests"] and info_sub[0] == 1:
        return False
    else:
        return True
