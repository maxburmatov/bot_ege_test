import sqlite3
from datetime import date

from aiogram.types import FSInputFile
from core.lexicon.lexicon import LEXICON_MEDIA

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()


async def admin_add_task_database(number, photo_task, photo_answer, answer):
    info = (number, photo_task, photo_answer, answer, 0, 0)
    cur.execute(
        f'INSERT INTO data_tasks (number_task, photo_task, photo_answer, answer, is_week, is_daily) VALUES (?, ?, ?, ?, ?, ?)',
        info)
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

    count_request = {"count_question_request": count_question_request, "count_error_request": count_error_request,
                     "count_error_task_request": count_error_task_request}

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
        info_request["photo_request"] = image

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

async def get_general_info_bots():
    info_dict = {}
    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) = 2')
    data = cur.fetchone()
    info_dict.update({"count_bots": data[0]})

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) = 2 and league_id = 1')
    data = cur.fetchone()
    info_dict.update({"count_bots_league_1": data[0]})

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) = 2 and league_id = 2')
    data = cur.fetchone()
    info_dict.update({"count_bots_league_2": data[0]})

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) = 2 and league_id = 3')
    data = cur.fetchone()
    info_dict.update({"count_bots_league_3": data[0]})

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) = 2 and league_id = 4')
    data = cur.fetchone()
    info_dict.update({"count_bots_league_4": data[0]})

    return info_dict

async def get_info_all_bots():
    info_list = []
    cur.execute(
        f'SELECT tg_id, name, points, league_id, avatar_id FROM students WHERE LENGTH(tg_id) = 2')
    bots = cur.fetchall()
    for bot in bots:
        info_bot = {}
        info_bot.update({"tg_id": bot[0]})
        info_bot.update({"name": bot[1]})
        info_bot.update({"points": bot[2]})
        info_bot.update({"league_id": bot[3]})
        info_bot.update({"avatar_id": bot[4]})
        info_list.append(info_bot)

    return info_list


async def admin_add_points(tg_id, points):
    cur.execute(
        f'UPDATE students SET points = points + {points} WHERE tg_id = {tg_id}')
    conn.commit()

async def admin_del_points(tg_id, points):
    cur.execute(
        f'UPDATE students SET points = points - {points} WHERE tg_id = {tg_id}')
    conn.commit()

async def admin_change_name(tg_id, name):
    cur.execute(
        f'UPDATE students SET name = "{name}" WHERE tg_id = {tg_id}')
    conn.commit()

async def admin_change_avatar(tg_id, avatar_id):
    cur.execute(
        f'UPDATE students SET avatar_id = {avatar_id} WHERE tg_id = {tg_id}')
    conn.commit()

async def admin_add_bot(tg_id, name, points, avatar_id, league_id):
    info = (tg_id, name, points, avatar_id, league_id)
    cur.execute(
        f'INSERT INTO students (tg_id, name, points, avatar_id, league_id) VALUES (?, ?, ?, ?, ?)',
        info)
    conn.commit()


async def get_general_daily_stats():
    date_today = str(date.today())
    stats_dict = {}

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students WHERE LENGTH(tg_id) > 2')
    data = cur.fetchone()
    stats_dict = {"count_all_students": data[0]}

    cur.execute(
        f'SELECT COUNT(date_start) FROM students WHERE date_start = "{date_today}"')
    data = cur.fetchone()
    stats_dict.update({"count_new_students": data[0]})

    cur.execute(
        f'SELECT COUNT(tg_id) FROM students_daily')
    data = cur.fetchone()
    stats_dict.update({"count_daily_active_students": data[0]})

    percent_active_daily_students = int(
        stats_dict["count_daily_active_students"] / stats_dict["count_all_students"] * 100)
    stats_dict.update({"percent_active_daily_students": f"{percent_active_daily_students}%"})

    cur.execute(f'SELECT SUM(tasks), SUM(tests), SUM(variants), SUM(daily_task) FROM students_daily')
    data = cur.fetchone()
    stats_dict.update({"count_tasks": data[0],
                       "count_tests": data[1],
                       "count_variants": data[2],
                       "count_daily_task": data[3],
                       })

    percent_count_daily_task = int(
        stats_dict["count_daily_task"] / stats_dict["count_daily_active_students"] * 100)
    stats_dict.update({"percent_count_daily_task": f"{percent_count_daily_task}%"})

    cur.execute(f'SELECT SUM(points), AVG(points), MAX(points) FROM students_daily')
    data = cur.fetchone()
    stats_dict.update({"sum_points": data[0],
                       "avg_points": data[1],
                       "max_points": data[2],
                       })

    cur.execute(f'SELECT tg_id FROM students_daily WHERE points = {stats_dict["max_points"]}')
    data = cur.fetchone()
    stats_dict.update({"leader_tg_id": data[0]})

    cur.execute(f'SELECT name, title_league FROM students JOIN league ON league_id = league.id WHERE tg_id = {stats_dict["leader_tg_id"]}')
    data = cur.fetchone()
    stats_dict.update({"leader_name": data[0],
                       "leader_title_league": data[1],
                       })

    cur.execute(
        f'SELECT COUNT(quests_id) FROM daily_quests_completed')
    data = cur.fetchone()
    stats_dict.update({"count_completed_daily_quests": data[0],
                       })

    cur.execute(
        f'SELECT COUNT(quests_id) FROM daily_quests_completed WHERE quests_id = 94')
    data = cur.fetchone()
    stats_dict.update({"count_completed_all_daily_quests": data[0],
                       })

    percent_completed_all_daily_quests = int(
        stats_dict["count_completed_all_daily_quests"] / stats_dict["count_daily_active_students"] * 100)
    stats_dict.update({"percent_completed_all_daily_quests": f"{percent_completed_all_daily_quests}%"})

    print(stats_dict)

    return stats_dict