import sqlite3

from datetime import datetime

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_status_sub(tg_id):
    cur.execute(
        f'SELECT is_sub, is_sub_date FROM sub WHERE tg_id = {tg_id}')

    stats = cur.fetchone()

    is_sub = stats[0]
    is_sub_date = stats[1]

    if is_sub == 0:
        status_sub = 'Неактивна'
    else:
        status_sub = 'Активна'
        date_sub = is_sub_date
        date_sub = date_sub[8:10] + date_sub[4:7] + date_sub[4:5] + date_sub[0:4]

    return status_sub