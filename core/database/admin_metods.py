import sqlite3

from aiogram.types import FSInputFile
from core.lexicon.lexicon import LEXICON_MEDIA

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()


async def admin_add_task_database(number, photo_task, photo_answer, answer):
    info = (number, photo_task, photo_answer, answer, 0, 0)
    cur.execute(f'INSERT INTO data_tasks (number_task, photo_task, photo_answer, answer, is_week, is_daily) VALUES (?, ?, ?, ?, ?, ?)', info)
    conn.commit()

async def admin_edit_task_database(task_id, number, photo_task, photo_answer, answer):
    cur.execute(
        f'UPDATE data_tasks SET number_task = {number}, photo_task = "{photo_task}", photo_answer = "{photo_answer}", answer = {answer} WHERE id = {task_id}')
    conn.commit()


async def get_task_info(task_id):
    cur.execute(
        f'select id, number_task, photo_task, photo_answer, answer, is_week, is_daily from data_tasks where id = {task_id}')
    task = cur.fetchone()

    task_dict = {"id": task[0], "number_task": task[1], "photo_task": task[2], "photo_answer": task[3],
                 "answer": task[4], "is_week": task[5], "is_daily": task[6]}

    return task_dict

async def get_count_new_request():
    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE status_request = "new"')
    data = cur.fetchone()

    count_new_request = data[0]

    return count_new_request

async def get_count_status_request():
    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE status_request = "new"')
    data = cur.fetchone()
    count_new_request = data[0]

    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE status_request = "finished"')
    data = cur.fetchone()
    count_finished_request = data[0]

    count_request = {"count_new_request": count_new_request, "count_finished_request": count_finished_request}

    return count_request

async def get_count_type_request(status_request):
    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE type_request = "question" and status_request = "{status_request}"')
    data = cur.fetchone()
    count_question_request = data[0]

    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE type_request = "error" and status_request = "{status_request}"')
    data = cur.fetchone()
    count_error_request = data[0]

    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE type_request = "error_task" and status_request = "{status_request}"')
    data = cur.fetchone()
    count_error_task_request = data[0]

    count_request = {"count_question_request": count_question_request, "count_error_request": count_error_request, "count_error_task_request": count_error_task_request}

    return count_request

async def get_request(counter, status_request, type_request):
    if status_request == 1:
        status_request = "new"
    elif status_request == 2:
        status_request = "finished"

    if type_request == 1:
        type_request = "question"
    elif type_request == 2:
        type_request = "error"
    elif type_request == 3:
        type_request = "error_task"

    cur.execute(
        f'SELECT COUNT(id) FROM users_requests WHERE status_request = "{status_request}" and type_request = "{type_request}"')
    data = cur.fetchone()
    count_requests = data[0]

    cur.execute(
        f'SELECT id, date_request, tg_id, type_request, text_request, photo_request, status_request, answer_request, comment_request '
        f'FROM users_requests WHERE status_request = "{status_request}" and type_request = "{type_request}"')
    data = cur.fetchall()
    request = data[counter]

    info_request = {"count_requests": count_requests, "id": request[0], "date_request": request[1],
                    "tg_id": request[2], "type_request": request[3], "text_request": request[4],
                    "photo_request": request[5], "status_request": request[6], "answer_request": request[7],
                    "comment_request": request[8]}

    if info_request["answer_request"] is None:
        info_request["answer_request"] = "Нету"

    if info_request["comment_request"] is None:
        info_request["comment_request"] = "Нету"

    if info_request["photo_request"] is None:
        path = LEXICON_MEDIA["no_photo_request"]
        image = FSInputFile(path)
        info_request["photo_request"] =  image

    return info_request


async def request_add_answer(id_request, answer):
    cur.execute(
        f'UPDATE users_requests SET answer_request = "{answer}" WHERE id = {id_request}')
    conn.commit()

async def request_mark_spam(id_request):
    cur.execute(
        f'UPDATE users_requests SET comment_request = "spam", status_request = "finished" WHERE id = {id_request}')
    conn.commit()

async def request_mark_finished(id_request):
    cur.execute(
        f'UPDATE users_requests SET status_request = "finished" WHERE id = {id_request}')
    conn.commit()

async def get_all_students_tg_id(id_request):
    cur.execute(
        f'UPDATE users_requests SET status_request = "finished" WHERE id = {id_request}')
    conn.commit()


