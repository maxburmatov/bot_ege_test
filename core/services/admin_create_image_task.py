from PIL import Image, ImageDraw, ImageFont
import os
import uuid

from aiogram.types import message
from core.database.metods.backpack_student import get_image_open_case
from core.lexicon.lexicon import LEXICON_CREATE_IMAGE_TASK


async def create_image_task():
    main_fill = (195, 233, 255)
    number_fill = (97, 185, 255)

    font_watermark = ImageFont.truetype('./font/Inter-Black.otf', size=40)
    font_number_task = ImageFont.truetype('./font/Inter-Black.otf', size=96)
    font_name_bot = ImageFont.truetype('./font/Inter-Black.otf', size=48)

    name_bot = LEXICON_CREATE_IMAGE_TASK["name"]
    link_bot = LEXICON_CREATE_IMAGE_TASK["link"]

    directory = "./media/templates/tasks"
    files = []
    files += os.listdir(directory)
    task_list = []
    for file in files:
        task_dict = {}
        file_dir = file
        file = file[0:-4]
        file = file.split("_")
        print(file)
        if file[0] == "task":
            task_dict["number"] = file[1]
            task_dict["task"] = file_dir
            for file2 in files:
                file2_dir = file2
                file2 = file2[0:-4]
                file2 = file2.split("_")
                print(file, file2)
                if file2[0] == "ris" and file[1] == file2[1] and file[2] == file2[2]:
                    task_dict["ris"] = file2_dir
                    break
                else:
                    task_dict["ris"] = "None"
                if file2[0] == "answer" and file[1] == file2[1] and file[2] == file2[2]:
                    task_dict["answer_image"] = f"./media/templates/tasks/{file2_dir}"
                    task_dict["answer"] = float(file2[3])
            task_list.append(task_dict)
    print(task_list)

    for task in task_list:
        number_task = task["number"]
        image_task = Image.open(f"./media/templates/tasks/{task["task"]}")
        image_bot = Image.open(f"./media/templates/image_bot.png")
        image_framing = Image.open(f"./media/templates/framing.png")
        width_image_task, height_image_task = image_task.size

        if task["ris"] == "None":
            width_template, height_template = width_image_task + 350, height_image_task
            width_framing, height_framing = image_framing.size
            width_image_bot, height_image_bot = image_bot.size
            link_bot_x, link_bot_y = 40, height_template - 80
            name_bot_x, name_bot_y = link_bot_x + 530, height_template - 85
            image_task_x, image_task_y = 190, -80
            number_task_x, number_task_y = 65, 30
            framing1_x, framing1_y = 0, 0
            framing2_x, framing2_y = width_template - width_framing, height_template - height_framing
            image_bot_x, image_bot_y = framing2_x + int((width_framing - width_image_bot) / 2), framing2_y + int(
                (height_framing - height_image_bot) / 2)

            image_template = Image.new('RGB', (width_template, height_template), 'white')

            image_template.paste(image_task, (image_task_x, image_task_y), mask=image_task)
            image_template.paste(image_framing, (framing1_x, framing1_y), mask=image_framing)
            image_template.paste(image_bot, (image_bot_x, image_bot_y), mask=image_bot)
            image_template.paste(image_framing, (framing2_x, framing2_y), mask=image_framing)
        else:
            picture_task = Image.open(f"./media/templates/tasks/{task["ris"]}")
            width_picture, height_picture = picture_task.size
            width_template, height_template = width_image_task + 350, height_image_task + height_picture

            width_framing, height_framing = image_framing.size
            width_image_bot, height_image_bot = image_bot.size

            link_bot_x, link_bot_y = 40, height_template - 80
            name_bot_x, name_bot_y = link_bot_x + 530, height_template-85
            image_task_x, image_task_y = 190, -80
            number_task_x, number_task_y = 65, 30
            picture_x, picture_y = image_task_x + int((width_image_task-width_picture)/2), height_image_task - 170
            framing1_x, framing1_y = 0, 0
            framing2_x, framing2_y = width_template - width_framing, height_template - height_framing
            image_bot_x, image_bot_y = framing2_x + int((width_framing-width_image_bot)/2), framing2_y + int((height_framing-height_image_bot)/2)

            image_template = Image.new('RGB', (width_template, height_template), 'white')

            image_template.paste(image_task, (image_task_x, image_task_y), mask=image_task)
            image_template.paste(image_framing, (framing1_x, framing1_y), mask=image_framing)
            image_template.paste(image_bot, (image_bot_x, image_bot_y), mask=image_bot)
            image_template.paste(image_framing, (framing2_x, framing2_y), mask=image_framing)
            image_template.paste(picture_task, (picture_x, picture_y), mask=picture_task)

        draw = ImageDraw.Draw(image_template)

        draw.text((name_bot_x, name_bot_y), name_bot, fill=main_fill, font=font_name_bot)
        draw.text((link_bot_x, link_bot_y), link_bot, fill=main_fill, font=font_watermark)
        draw.text((number_task_x, number_task_y), number_task, fill=number_fill, font=font_number_task)

        path = f'./media/templates/results/{task["task"]}'

        image_template.save(path, quality=100)

        task["task_image"] = path

    print(task_list)
    return task_list
