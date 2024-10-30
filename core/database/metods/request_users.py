import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def add_request(date_request, tg_id, type_request, text_request, photo_request, status_request):
    date_request = str(date_request)
    date_request = date_request[0:19]
    format_date_request = datetime.strptime(date_request, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)

    info = (format_date_request, tg_id, type_request, text_request, photo_request, status_request)
    cur.execute(f'INSERT INTO users_requests (date_request, tg_id, type_request, text_request, photo_request, status_request) VALUES (?, ?, ?, ?, ?, ?)', info)
    conn.commit()