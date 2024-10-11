import sqlite3

from datetime import date, datetime, timedelta

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def check_add_student(user_id):
    cur.execute(f'SELECT tg_id FROM users WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        return True
    else:
        return False


async def add_student(user_id, name, purpose, invited_tg_id):
    cur.execute(f'SELECT tg_id FROM users WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 3)
        cur.execute(
            f"INSERT INTO users (tg_id, role_id) VALUES (?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM students WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (user_id, name, purpose, 1, 1, 0, date.today(), invited_tg_id, 0, 1, 0)
        cur.execute(
            f"INSERT INTO students (tg_id, name, purpose_id, league_id, avatar_id, points, date_start, invited_tg_id, days_in_row, is_active, stars) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM students_daily WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 0, 0, 0, 0, 0, 0)
        cur.execute(
            f"INSERT INTO students_daily (tg_id, tasks, tests, variants, weekly_var, daily_task, collect_daily_points) VALUES (?, ?, ?, ?, ?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM general_stats_students WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 0, 0, 0, 0, 0, 0, 0)
        cur.execute(
            f"INSERT INTO general_stats_students (tg_id, tasks, tasks_time, tests, tests_r, variants, variants_r, variants_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM sub WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 0, 0, 0, 0)
        cur.execute(
            f"INSERT INTO sub (tg_id, demo_sub, demo_sub_date, is_sub, is_sub_date) VALUES (?, ?, ?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM stats_students_tasks WHERE tg_id = {user_id}')
    data = cur.fetchone()
    if data is None:
        info = (
            user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cur.execute(
            f"INSERT INTO stats_students_tasks (tg_id, prev_proc_1_r, prev_proc_2_r, prev_proc_3_r, prev_proc_4_r, prev_proc_5_r, prev_proc_6_r, prev_proc_7_r, prev_proc_8_r, prev_proc_9_r, prev_proc_10_r, prev_proc_11_r, prev_proc_12_r, "
            f"new_proc_1_r, new_proc_2_r, new_proc_3_r, new_proc_4_r, new_proc_5_r, new_proc_6_r, new_proc_7_r, new_proc_8_r, new_proc_9_r, new_proc_10_r, new_proc_11_r, new_proc_12_r, "
            f"task_1, task_1_r, task_time_1, task_2, task_2_r, task_time_2, task_3, task_3_r, task_time_3, task_4, task_4_r, task_time_4, task_5, task_5_r, task_time_5, task_6, task_6_r, task_time_6, task_7, task_7_r, task_time_7, "
            f"task_8, task_8_r, task_time_8, task_9, task_9_r, task_time_9, task_10, task_10_r, task_time_10, task_11, task_11_r, task_time_11, task_12, task_12_r, task_time_12) "
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            f"?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM students_inventory WHERE tg_id = {user_id} and item_id = 1')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 1, 1)
        cur.execute(
            f"INSERT INTO students_inventory (tg_id, item_id, item_count) VALUES (?, ?, ?)",
            info)
        conn.commit()

    cur.execute(f'SELECT tg_id FROM students_inventory WHERE tg_id = {user_id} and item_id = 2')
    data = cur.fetchone()
    if data is None:
        info = (user_id, 2, 1)
        cur.execute(
            f"INSERT INTO students_inventory (tg_id, item_id, item_count) VALUES (?, ?, ?)",
            info)
        conn.commit()