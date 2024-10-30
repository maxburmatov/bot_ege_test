import sqlite3

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()


async def db_start():
    """создание БД"""
    cur.execute('CREATE TABLE IF NOT EXISTS users('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'role_id INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS students('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'name TEXT, '
                'points INTEGER, '
                'purpose_id INTEGER, '
                'league_id INTEGER, '
                'date_start TEXT,'
                'avatar_id INTEGER, '
                'invited_tg_id INTEGER, '
                'days_in_row INTEGER, '
                'is_active INTEGER, '
                'stars INTEGER,'
                'boost TEXT, '
                'usdt float, '
                'uts_time INTEGER, '
                'days_no_active INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS sub('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'demo_sub INTEGER, '
                'demo_sub_date TEXT, '
                'is_sub INTEGER, '
                'is_sub_date TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS students_daily('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tasks INTEGER, '
                'tests INTEGER, '
                'variants INTEGER, '
                'weekly_var INTEGER,'
                'daily_task INTEGER, '
                'collect_daily_points INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS general_stats_students('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tasks INTEGER, '
                'tasks_time INTEGER, '
                'tests INTEGER, '
                'tests_r INTEGER, '
                'variants INTEGER, '
                'variants_r INTEGER, '
                'variants_time INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS stats_students_tasks('
                'tg_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'task_1 INTEGER, task_1_r INTEGER, prev_proc_1_r FLOAT, new_proc_1_r FLOAT, task_time_1 INTEGER, '
                'task_2 INTEGER, task_2_r INTEGER, prev_proc_2_r FLOAT, new_proc_2_r FLOAT, task_time_2 INTEGER,'
                'task_3 INTEGER, task_3_r INTEGER, prev_proc_3_r FLOAT, new_proc_3_r FLOAT, task_time_3 INTEGER,'
                'task_4 INTEGER, task_4_r INTEGER, prev_proc_4_r FLOAT, new_proc_4_r FLOAT, task_time_4 INTEGER,'
                'task_5 INTEGER, task_5_r INTEGER, prev_proc_5_r FLOAT, new_proc_5_r FLOAT, task_time_5 INTEGER,'
                'task_6 INTEGER, task_6_r INTEGER, prev_proc_6_r FLOAT, new_proc_6_r FLOAT, task_time_6 INTEGER,'
                'task_7 INTEGER, task_7_r INTEGER, prev_proc_7_r FLOAT, new_proc_7_r FLOAT, task_time_7 INTEGER,'
                'task_8 INTEGER, task_8_r INTEGER, prev_proc_8_r FLOAT, new_proc_8_r FLOAT, task_time_8 INTEGER,'
                'task_9 INTEGER, task_9_r INTEGER, prev_proc_9_r FLOAT, new_proc_9_r FLOAT, task_time_9 INTEGER,'
                'task_10 INTEGER, task_10_r INTEGER, prev_proc_10_r FLOAT, new_proc_10_r FLOAT, task_time_10 INTEGER,'
                'task_11 INTEGER, task_11_r INTEGER, prev_proc_11_r FLOAT, new_proc_11_r FLOAT, task_time_11 INTEGER,'
                'task_12 INTEGER, task_12_r INTEGER, prev_proc_12_r FLOAT, new_proc_12_r FLOAT, task_time_12 INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS league('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_league TEXT, '
                'count_students INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS league_prize('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'league_id INTEGER, '
                'place INTEGER, '
                'prize_points INTEGER, '
                'item_id INTEGER, '
                'count_item INTEGER, '
                'stars INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS daily_quests('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_quests TEXT, '
                'type_quest TEXT, '
                'type_prize TEXT, '
                'points_quest INTEGER,'
                'item_id INTEGER, '
                'count_item INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS other_quests('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_quests TEXT, '
                'type_quest TEXT, '
                'type_prize TEXT, '
                'points_quest INTEGER,'
                'item_id INTEGER, '
                'is_repeat INTEGER, '
                'count_item INTEGER, '
                'next_quest_id INTEGER, '
                'need_league_id INTEGER, '
                'start_quest INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS students_daily_quest('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'quests_id INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS students_other_quest('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'quests_id INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS daily_quests_completed('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'quests_id INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS other_quests_completed('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'quests_id INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS roles('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_role TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS data_tasks('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'number_task INTEGER,'
                'photo_task TEXT,'
                'photo_answer TEXT,'
                'answer FLOAT, '
                'is_week INTEGER,'
                'is_daily INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS students_daily_temp('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'action TEXT, '
                'number INTEGER, '
                'count_all INTEGER, '
                'count_r INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS cases('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_case TEXT,'
                'image_case TEXT,'
                'image_open_case TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS items_case('
                'case_id INTEGER, '
                'item_id INTEGER, '
                'weight_item FLOAT)')

    cur.execute('CREATE TABLE IF NOT EXISTS items_all('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'title_item TEXT, '
                'image_item TEXT, '
                'image_backpack TEXT, '
                'type_item TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS items_shop('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'item_id INTEGER, '
                'title_item TEXT, '
                'display_name TEXT, '
                'image_item TEXT, '
                'price TEXT, '
                'payload TEXT, '
                'count INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS students_inventory('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'item_id INTEGER, '
                'item_count INTEGER)')

    cur.execute('CREATE TABLE IF NOT EXISTS users_requests('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'date_request TEXT,'
                'tg_id INTEGER, '
                'type_request TEXT,'
                'text_request TEXT, '
                'photo_request TEXT, '
                'status_request TEXT,'
                'answer_request TEXT,'
                'comment_request TEXT)')

    conn.commit()


