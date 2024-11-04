import sqlite3

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

async def get_backpack_items(tg_id, type_item):
    cur.execute(
        f'SELECT title_item, image_backpack, item_count, item_id FROM students_inventory JOIN items_all ON items_all.id = item_id WHERE tg_id = {tg_id} and type_item = "{type_item}"')
    data = cur.fetchall()
    items = []
    for item in data:
        title_item = item[0]
        title_item = title_item.replace("-", " ")

        dict_item = {'title_item' : title_item, 'image_backpack' : item[1], 'count_item' : item[2], 'item_id' : item[3]}

        items.append(dict_item)
    print(items)
    return items

async def get_case_id(item_id):
    cur.execute(
        f'SELECT id FROM cases WHERE title_case = (SELECT title_item FROM students_inventory JOIN items_all ON item_id = items_all.id WHERE item_id = {item_id})')
    data = cur.fetchone()
    case_id = data[0]

    return case_id
async def get_image_open_case(item_id):
    case_id = await get_case_id(item_id)
    cur.execute(
        f'SELECT image_open_case FROM cases WHERE cases.id = {case_id}')
    data = cur.fetchone()
    image_open_case = data[0]

    print(image_open_case)

    return image_open_case

async def get_items_from_case(case_id):
    cur.execute(
        f'SELECT items_all.id, title_item, image_item, type_item, weight_item FROM items_case JOIN items_all ON items_case.item_id = items_all.id WHERE case_id = {case_id}')
    data = cur.fetchall()
    info_case = []

    for item in data:
        item_image = f"./core/media/case/{item[2]}"
        dict_item = {'item_id': item[0], 'title_item': item[1], 'image_item': item_image, 'type_item': item[3], 'weight_item': item[4]}
        info_case.append(dict_item)

    return info_case


async def get_info_case(item_id):

    case_id = await get_case_id(item_id)
    info_case = await get_items_from_case(case_id)

    return info_case


async def get_image_avatar_profile(item_id):

    cur.execute(
        f'SELECT image_item FROM items_all WHERE id = {item_id}')
    stats = cur.fetchone()

    avatar_title = stats[0]
    avatar_image = f"./core/media/avatars_profile/{avatar_title}"

    return avatar_image

async def add_item_in_backpack(tg_id, item_id, count):
    cur.execute(f'SELECT tg_id FROM students_inventory WHERE tg_id = {tg_id} and item_id = {item_id}')
    data = cur.fetchone()
    if data is None:
        info = (tg_id, item_id, count)
        cur.execute(f'INSERT INTO students_inventory (tg_id, item_id, item_count) VALUES (?, ?, ?)',
                info)
    else:
        cur.execute(
            f'UPDATE students_inventory SET item_count = item_count + {count} WHERE tg_id = {tg_id} and item_id = {item_id}')
    conn.commit()
    print("Предмет добавлен!")

async def delete_item_in_backpack(tg_id, item_id):
    cur.execute(
        f'SELECT item_count FROM students_inventory JOIN items_all ON item_id = items_all.id WHERE tg_id = {tg_id} AND item_id = {item_id}')
    data = cur.fetchone()
    count_item = data[0]
    if count_item == 1:
        cur.execute(
            f'DELETE FROM students_inventory WHERE tg_id = {tg_id} AND item_id = {item_id}')
    else:
        cur.execute(
            f'UPDATE students_inventory SET item_count = item_count - 1 WHERE tg_id = {tg_id} AND item_id = {item_id}')

    conn.commit()

async def get_title_item(item_id):
    cur.execute(
        f'SELECT title_item FROM items_all WHERE id = {item_id}')
    data = cur.fetchone()
    title_item = data[0]
    title_item = title_item.replace("-", " ")
    print(title_item)
    return title_item
