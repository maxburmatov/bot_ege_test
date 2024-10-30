import sqlite3

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_random_tasks(number, type_module):
    data_task = []
    all_tasks = ()
    if type_module == "task":
        if number == 0:
            cur.execute(f'select id, number_task, photo_task, photo_answer, answer from data_tasks where is_week = 0 and is_daily = 0 ORDER BY random()')
            all_tasks = cur.fetchall()
        else:
            cur.execute(
                f'select id, number_task, photo_task, photo_answer, answer from data_tasks where is_week = 0 and is_daily = 0 and number_task = {number} ORDER BY random()')
            all_tasks = cur.fetchall()
    elif type_module == "test":
        cur.execute(
            f'select id, number_task, photo_task, photo_answer, answer from data_tasks where is_week = 0 and is_daily = 0 and number_task = {number} ORDER BY random() LIMIT 5')
        all_tasks = cur.fetchall()

    for task in all_tasks:
        task_dict = {"id": task[0], "number_task": task[1], "photo_task": task[2], "photo_answer": task[3], "answer": task[4]}
        data_task.append(task_dict)

    print(data_task)
    return data_task

async def get_daily_task():
    cur.execute(f'SELECT id FROM data_tasks WHERE is_daily = 1')
    data = cur.fetchone()
    current_daily_task = data[0]

    cur.execute(
        f'select id, number_task, photo_task, photo_answer, answer from data_tasks where id = {current_daily_task}')
    task = cur.fetchone()

    task_dict = {"id": task[0], "number_task": task[1], "photo_task": task[2], "photo_answer": task[3],
                 "answer": task[4]}

    return task_dict