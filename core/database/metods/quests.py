import sqlite3

import random

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_count_quests_completed(tg_id):
    cur.execute(
        f'SELECT COUNT(*) FROM quests_completed WHERE tg_id = {tg_id}')
    stats = cur.fetchone()

    count_quests = stats[0]

    return count_quests

async def generate_daily_quests(tg_id):

    daily_quests = []

    cur.execute(f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests JOIN quests_completed ON quests.id = quests_id WHERE category_quest = "daily" and type_quest = "task" and quests_completed.tg_id = {tg_id}')
    st_quest_completed = cur.fetchall()

    print(st_quest_completed)

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests WHERE category_quest = "daily" and type_quest = "task"')
    all_quests = cur.fetchall()

    print(all_quests)

    random.shuffle(all_quests)

    if st_quest_completed is None:
        id_task_quest = all_quests[0]
    else:
        all_quests = [x for x in all_quests if not x in st_quest_completed]
        id_task_quest = all_quests[0]

    print(id_task_quest)

    daily_quests.append(id_task_quest)

    print(daily_quests)

    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests JOIN quests_completed ON quests.id = quests_id WHERE category_quest = "daily" and type_quest = "test" and quests_completed.tg_id = {tg_id}')
    st_quest_completed = cur.fetchall()

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests WHERE category_quest = "daily" and type_quest = "test"')
    all_quests = cur.fetchall()

    random.shuffle(all_quests)

    if st_quest_completed is None:
        id_test_quest = all_quests[0]
    else:
        all_quests = [x for x in all_quests if not x in st_quest_completed]
        id_test_quest = all_quests[0]

    daily_quests.append(id_test_quest)

    print(all_quests)
    print(id_test_quest)

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests WHERE category_quest = "daily" and type_quest = "var"')
    all_quests = cur.fetchall()

    random.shuffle(all_quests)
    id_var_quest = all_quests[0]

    daily_quests.append(id_var_quest)

    print(all_quests)
    print(id_var_quest)

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id FROM quests WHERE category_quest = "daily" and type_quest = "every_day"')
    all_quests = cur.fetchone()
    id_every_day_quest = all_quests

    daily_quests.append(id_every_day_quest)

    print(all_quests)
    print(id_every_day_quest)
    print(daily_quests)

    for i in daily_quests:
        info = (tg_id, int(i[0]))
        print(info)
        cur.execute(f'INSERT INTO students_daily_quest (tg_id, quests_id) VALUES (?, ?)', info)
        conn.commit()

    return daily_quests

async def check_generate_daily_quests(tg_id):
    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id FROM students_daily_quest JOIN quests ON quests.id = quests_id WHERE category_quest = "daily" and tg_id = {tg_id}')
    check_daily_quests = cur.fetchall()
    print(check_daily_quests)
    if not check_daily_quests:
        print(False)
        return False
    else:
        print(True)
        return True

async def get_daily_quests(tg_id):
    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id FROM students_daily_quest JOIN quests ON quests.id = quests_id WHERE category_quest = "daily" and tg_id = {tg_id}')
    check_daily_quests = cur.fetchall()

    return check_daily_quests

async def check_quest_completed(tg_id, quests_id):
    cur.execute(f'SELECT * FROM quests_completed WHERE tg_id = {tg_id} and quests_id = {quests_id}')
    data = cur.fetchone()
    if data is None:
        return True
    else:
        return False

async def add_quest_completed(tg_id, quests_id):
    info = (tg_id, quests_id)
    cur.execute(f'INSERT INTO quests_completed (tg_id, quests_id) VALUES (?, ?)', info)
    conn.commit()