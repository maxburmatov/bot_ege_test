import sqlite3
from datetime import date

from core.database.metods.admin_metods import get_general_daily_stats

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def save_general_daily_stats():
    # OTDELRAZRABOTKI-24
    date_today = str(date.today())

    stats_dict = await get_general_daily_stats()

    info = (date_today,
            stats_dict["count_all_students"],
            stats_dict["count_new_students"],
            stats_dict["count_daily_active_students"],
            stats_dict["count_tasks"],
            stats_dict["count_daily_task"],
            stats_dict["count_tests"],
            stats_dict["count_variants"],
            stats_dict["sum_points"],
            int(stats_dict["avg_points"]),
            stats_dict["max_points"],
            stats_dict["leader_tg_id"],

            )
    cur.execute(
        f"INSERT INTO users (tg_id, role_id) VALUES (?, ?)",
        info)
    conn.commit()

