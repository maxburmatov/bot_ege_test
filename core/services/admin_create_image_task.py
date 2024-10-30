from PIL import Image, ImageDraw, ImageFont

import uuid

from core.database.metods.backpack_student import get_image_open_case
from core.lexicon.lexicon import LEXICON_CREATE_IMAGE_TASK


async def create_prize_image(number_task):
    image = await get_image_open_case(item_id)
    image_open_case = Image.open(image)

    draw = ImageDraw.Draw(image_open_case)
    font = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=52)

    name_bot_x, name_bot_y = 920, 1940
    link_bot_x, link_bot_y = 920, 1940
    watermark_x, watermark_y = 920, 1940
    number_task_x, number_task_y = 920, 2000
    image_task_x, image_task_y = 920, 1520
    picture_x, picture_y = 920, 1520

    name_bot = LEXICON_CREATE_IMAGE_TASK["name"]
    link_bot = LEXICON_CREATE_IMAGE_TASK["link"]
    watermark = LEXICON_CREATE_IMAGE_TASK["link"]

    str_title = prize1['title_item']
    str_title = str_title.split("-")

    draw.text((title1_x, title1_y), f'{str_title[0]}', fill='white', font=font)
    draw.text((title2_x, title2_y), f'{str_title[1]}', fill='white', font=font)

    image_avatar = Image.open(f'{prize['image_item']}')
    image_open_case.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

    image_open_case.save(f'./media/temp/{random_str}.png', quality=100)

    path = f'./media/temp/{random_str}.png'

    return path