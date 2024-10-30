import sqlite3

import random

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()


async def get_count_quests_completed(tg_id):
    cur.execute(
        f'SELECT COUNT(*) FROM daily_quests_completed WHERE tg_id = {tg_id}')
    stats = cur.fetchone()
    count_daily_quests = stats[0]

    cur.execute(
        f'SELECT COUNT(*) FROM other_quests_completed WHERE tg_id = {tg_id}')
    stats = cur.fetchone()
    count_other_quests = stats[0]

    count_quests = count_daily_quests + count_other_quests

    return count_quests


async def generate_daily_quests(tg_id):
    daily_quests = []

    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests JOIN daily_quests_completed ON daily_quests.id = quests_id WHERE type_quest = "task" and daily_quests_completed.tg_id = {tg_id}')
    st_quest_completed = cur.fetchall()

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests WHERE type_quest = "task" ORDER BY RANDOM()')
    all_quests = cur.fetchall()

    if st_quest_completed is None:
        id_task_quest = all_quests[0]
    else:
        all_quests = [x for x in all_quests if not x in st_quest_completed]
        id_task_quest = all_quests[0]

    print(id_task_quest)

    dict_task_quest = {"quests_id": id_task_quest[0], "title_quests": id_task_quest[1], "type_quest": id_task_quest[2],
                       "type_prize": id_task_quest[3],
                       "points_quest": id_task_quest[4], "item_id": id_task_quest[5], "count_item": id_task_quest[6]}

    daily_quests.append(dict_task_quest)

    print(daily_quests)

    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests JOIN daily_quests_completed ON daily_quests.id = quests_id WHERE type_quest = "test" and daily_quests_completed.tg_id = {tg_id}')
    st_quest_completed = cur.fetchall()

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests WHERE type_quest = "test" ORDER BY RANDOM()')
    all_quests = cur.fetchall()

    if st_quest_completed is None:
        id_test_quest = all_quests[0]
    else:
        all_quests = [x for x in all_quests if not x in st_quest_completed]
        id_test_quest = all_quests[0]

    dict_test_quest = {"quests_id": id_test_quest[0], "title_quests": id_test_quest[1], "type_quest": id_test_quest[2],
                       "type_prize": id_test_quest[3],
                       "points_quest": id_test_quest[4], "item_id": id_test_quest[5], "count_item": id_test_quest[6]}

    daily_quests.append(dict_test_quest)

    print(all_quests)
    print(id_test_quest)

    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests JOIN daily_quests_completed ON daily_quests.id = quests_id WHERE (type_quest = "var" and daily_quests_completed.tg_id = {tg_id}) or (type_quest = "daily_task" and daily_quests_completed.tg_id = {tg_id})')
    st_quest_completed = cur.fetchall()

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests WHERE type_quest = "var" or type_quest = "daily_task" ORDER BY RANDOM()')
    all_quests = cur.fetchall()

    if st_quest_completed is None:
        id_mix_quest = all_quests[0]
    else:
        all_quests = [x for x in all_quests if not x in st_quest_completed]
        id_mix_quest = all_quests[0]

    dict_mix_quest = {"quests_id": id_mix_quest[0], "title_quests": id_mix_quest[1], "type_quest": id_mix_quest[2],
                      "type_prize": id_mix_quest[3],
                      "points_quest": id_mix_quest[4], "item_id": id_mix_quest[5], "count_item": id_mix_quest[6]}

    daily_quests.append(dict_mix_quest)

    print(all_quests)
    print(id_mix_quest)

    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM daily_quests WHERE type_quest = "every_day"')
    all_quests = cur.fetchone()
    id_every_day_quest = all_quests

    dict_every_day_quest = {"quests_id": id_every_day_quest[0], "title_quests": id_every_day_quest[1],
                            "type_quest": id_every_day_quest[2], "type_prize": id_every_day_quest[3],
                            "points_quest": id_every_day_quest[4], "item_id": id_every_day_quest[5],
                            "count_item": id_every_day_quest[6]}

    daily_quests.append(dict_every_day_quest)

    print(all_quests)
    print(id_every_day_quest)
    print(daily_quests)

    for i in daily_quests:
        info = (tg_id, i["quests_id"])
        print(info)
        cur.execute(f'INSERT INTO students_daily_quest (tg_id, quests_id) VALUES (?, ?)', info)
        conn.commit()

    return daily_quests


async def generate_other_quests(tg_id):
    cur.execute(
        f'SELECT id, title_quests, type_quest, type_prize, points_quest, item_id, is_repeat, count_item, next_quest_id, need_league_id, start_quest FROM other_quests WHERE start_quest = 1')
    data = cur.fetchall()

    list_other_quest = []
    for quest in data:
        dict_quest = {"quests_id": quest[0], "title_quests": quest[1],
                      "type_quest": quest[2], "type_prize": quest[3],
                      "points_quest": quest[4], "item_id": quest[5],
                      "is_repeat": quest[6], "count_item": quest[7],
                      "next_quest_id": quest[8], "need_league_id": quest[9],
                      "start_quest": quest[10]
                      }
        info = (tg_id, dict_quest["quests_id"])
        cur.execute(f'INSERT INTO students_other_quest (tg_id, quests_id) VALUES (?, ?)', info)
        conn.commit()
        list_other_quest.append(dict_quest)

    return list_other_quest


async def check_generate_daily_quests(tg_id):
    cur.execute(
        f'SELECT COUNT(id) FROM students_daily_quest WHERE tg_id = {tg_id}')
    check_daily_quests = cur.fetchone()
    count_daily_quests = check_daily_quests[0]

    if count_daily_quests != 4:
        return False
    else:
        return True


async def check_generate_other_quests(tg_id):
    cur.execute(
        f'SELECT COUNT(id) FROM students_other_quest WHERE tg_id = {tg_id}')
    check_other_quests = cur.fetchone()
    count_other_quests = check_other_quests[0]

    if count_other_quests == 0:
        return False
    else:
        return True


async def get_daily_quests(tg_id):
    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id, count_item FROM students_daily_quest JOIN daily_quests ON daily_quests.id = quests_id WHERE tg_id = {tg_id}')
    data = cur.fetchall()
    list_daily_quest = []
    for quest in data:
        dict_quest = {"quests_id": quest[0], "title_quests": quest[1],
                      "type_quest": quest[2], "type_prize": quest[3],
                      "points_quest": quest[4], "item_id": quest[5],
                      "count_item": quest[6]}
        list_daily_quest.append(dict_quest)

    return list_daily_quest


async def get_other_quests(tg_id):
    cur.execute(
        f'SELECT quests_id, title_quests, type_quest, type_prize, points_quest, item_id, is_repeat, count_item, next_quest_id, need_league_id, start_quest FROM students_other_quest JOIN other_quests ON other_quests.id = quests_id WHERE tg_id = {tg_id}')
    data = cur.fetchall()
    list_other_quest = []
    for quest in data:
        dict_quest = {"quests_id": quest[0], "title_quests": quest[1],
                      "type_quest": quest[2], "type_prize": quest[3],
                      "points_quest": quest[4], "item_id": quest[5],
                      "is_repeat": quest[6], "count_item": quest[7],
                      "next_quest_id": quest[8], "need_league_id": quest[9],
                      "start_quest": quest[10]
                      }
        list_other_quest.append(dict_quest)

    return list_other_quest


async def check_quest_completed(tg_id, quests_id, category_quest):
    if category_quest == "daily":
        cur.execute(f'SELECT * FROM daily_quests_completed WHERE tg_id = {tg_id} and quests_id = {quests_id}')
        data = cur.fetchone()
    else:
        cur.execute(f'SELECT * FROM other_quests_completed WHERE tg_id = {tg_id} and quests_id = {quests_id}')
        data = cur.fetchone()

    if data is None:
        return True
    else:
        return False


async def add_quest_completed(tg_id, quests_id, type_quest):
    if type_quest == "daily":
        info = (tg_id, quests_id)
        cur.execute(f'INSERT INTO daily_quests_completed (tg_id, quests_id) VALUES (?, ?)', info)
        conn.commit()
    else:
        info = (tg_id, quests_id)
        cur.execute(f'INSERT INTO other_quests_completed (tg_id, quests_id) VALUES (?, ?)', info)
        conn.commit()


async def add_student_quest(tg_id, quest_id, next_quest_id):
    info = (tg_id, next_quest_id)
    cur.execute(f'DELETE from students_other_quest WHERE quests_id = {quest_id}')
    cur.execute(f'INSERT INTO students_other_quest(tg_id, quests_id) VALUES (?, ?)', info)
    conn.commit()


async def delete_student_quest(tg_id, quest_id):
    cur.execute(f'DELETE from students_other_quest WHERE quests_id = {quest_id}')
    conn.commit()
