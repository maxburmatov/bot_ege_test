import sqlite3

from datetime import datetime

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_daily_stats_student(tg_id):
    cur.execute(
        f'SELECT tasks, tests, variants FROM students_daily WHERE tg_id = {tg_id}')

    stats = cur.fetchone()

    tasks_daily = stats[0]
    tests_daily = stats[1]
    variants_daily = stats[2]

    stats_daily_student = {"tasks_daily": tasks_daily, "tests_daily": tests_daily, "variants_daily": variants_daily}

    return stats_daily_student

async def get_general_stats_student(tg_id):
    cur.execute(
        f'SELECT tasks, tests, tests_r, variants, variants_r, tasks_time, variants_time FROM general_stats_students WHERE tg_id = {tg_id}')

    stats = cur.fetchone()

    tasks = stats[0]
    tests = stats[1]
    tests_r = stats[2]
    variants = stats[3]
    variants_r = stats[4]
    tasks_time = stats[5]
    variants_time = stats[6]

    if tasks_time != 0:
        avarage_tasks_time = tasks_time // tasks
    else:
        avarage_tasks_time = 0

    if avarage_tasks_time < 60:
        time_task = f"{avarage_tasks_time} сек."
    elif avarage_tasks_time < 3600:
        min = avarage_tasks_time // 60
        sec = avarage_tasks_time - min * 60
        time_task = f"{min} мин. {sec} сек."
    else:
        hour = avarage_tasks_time // 3600
        min = (avarage_tasks_time - hour * 3600) // 60
        sec = avarage_tasks_time - min * 60 - hour * 3600
        time_task = f"{hour} ч. {min} мин. {sec} сек."

    if tests == 0:
        percent_test = 0
    else:
        percent_test = round(tests_r / (tests * 5) * 100, 1)

    if variants == 0:
        percent_var = 0
    else:
        percent_var = round(variants_r / (variants * 19) * 100, 1)

    stats_general_student = {"tasks": tasks, "tests": tests, "variants": variants, "percent_test": percent_test,
                             "percent_var": percent_var, "time_task": time_task}

    return stats_general_student

async def add_stat_tasks(user_id, task, value):
    cur.execute(
        f'UPDATE stats_students_tasks SET task_{task} = task_{task} + 1, task_{task}_r = task_{task}_r + {value} WHERE tg_id = {user_id}')
    conn.commit()

    cur.execute(
        f'SELECT task_{task}, task_{task}_r, prev_proc_{task}_r, new_proc_{task}_r FROM stats_students_tasks WHERE tg_id = {user_id}')
    info = cur.fetchone()

    if info[0] == 5:
        prev_proc = round(info[1] / info[0] * 100, 1)
        cur.execute(
            f'UPDATE stats_students_tasks SET prev_proc_{task}_r = {prev_proc} WHERE tg_id = {user_id}')
        conn.commit()

    if info[0] == 10:
        new_proc = round(info[1] / info[0] * 100, 1)
        cur.execute(
            f'UPDATE stats_students_tasks SET new_proc_{task}_r = {new_proc} WHERE tg_id = {user_id}')
        conn.commit()

    if info[0] > 10 and info[0] % 5 == 0:
        new_proc = round(info[1] / info[0] * 100, 1)
        prev_proc = info[3]
        cur.execute(
            f'UPDATE stats_students_tasks SET prev_proc_{task}_r = {prev_proc}, new_proc_{task}_r = {new_proc} WHERE tg_id = {user_id}')
        conn.commit()