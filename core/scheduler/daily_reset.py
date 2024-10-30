import sqlite3
from datetime import date, datetime, timedelta

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()


async def reset_daily_stats():
    # Дневное задание
    data_today = date.today()
    cur.execute(f'UPDATE students_daily SET tasks = 0, variants = 0, tests = 0, weekly_var = 0, daily_task = 0, collect_daily_points = 0')
    cur.execute(f'UPDATE sub SET is_sub = 0, is_sub_date = 0 WHERE is_sub_date = "{data_today}"')
    cur.execute(f'DELETE FROM students_daily_temp')
    cur.execute(f'DELETE FROM students_daily_quest')
    conn.commit()

    # Дневное задание
    cur.execute(f'SELECT id FROM data_tasks WHERE is_daily = 1')
    data = cur.fetchone()
    current_daily_task = data[0]

    cur.execute(f'SELECT id FROM data_tasks WHERE id != {current_daily_task} ORDER BY random() LIMIT 1')
    data = cur.fetchone()
    new_daily_task = data[0]

    cur.execute(f'UPDATE data_tasks SET is_daily = 0 WHERE id = {current_daily_task}')
    cur.execute(f'UPDATE data_tasks SET is_daily = 1 WHERE id = {new_daily_task}')

    conn.commit()
