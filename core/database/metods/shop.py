import sqlite3

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_shop_case(page):
    info_case = {}
    cur.execute(
            f'SELECT DISTINCT item_id, title_item FROM items_shop ORDER BY title_item')
    data = cur.fetchall()
    case = data[page]
    case_item_id = case[0]
    title_item = case[1]
    count_cases = len(data)
    info_case['case_item_id'] = case_item_id
    info_case['title_item '] = title_item

    cur.execute(
        f'SELECT item_id, title_item, display_name, image_item, price, payload, count FROM items_shop WHERE item_id = {info_case['case_item_id']}')
    case_data = cur.fetchall()

    info_case['cases_data'] = case_data

    return count_cases, info_case