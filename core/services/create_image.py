from PIL import Image, ImageDraw, ImageFont

import uuid

from core.database.metods.backpack_student import get_image_open_case


async def create_prize_image(item_id, prize):
    image = await get_image_open_case(item_id)
    image_open_case = Image.open(image)

    draw = ImageDraw.Draw(image_open_case)
    font = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=52)

    title1_x, title1_y = 920, 1940
    title2_x, title2_y = 920, 2000
    avatar_x, avatar_y = 920, 1520

    random_str = str(uuid.uuid4())
    random_str = random_str[:10]

    str_title = prize['title_item']
    str_title = str_title.split("-")

    draw.text((title1_x, title1_y), f'{str_title[0]}', fill='white', font=font)
    draw.text((title2_x, title2_y), f'{str_title[1]}', fill='white', font=font)

    image_avatar = Image.open(f'{prize['image_item']}')
    image_open_case.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

    image_open_case.save(f'./media/temp/{random_str}.png', quality=100)

    path = f'./media/temp/{random_str}.png'

    return path


async def create_room_image(info_student, stats_daily_student, stats_general_student, info_league):
    image_room_stats = Image.open('./media/room_stats.png')

    draw = ImageDraw.Draw(image_room_stats)

    font = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=36)
    font_league = ImageFont.truetype('./font/Montserrat-Bold.ttf', size=36)
    font2 = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=40)
    font_count = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=96)

    main_fill = (8, 61, 130)
    league1_fill = (31, 201, 62)
    league2_fill = (67, 92, 155)
    league3_fill = (208, 87, 255)
    league4_fill = (255, 84, 105)

    league_id = info_student.get("league_id")

    match league_id:
        case 1:
            league_fill = league1_fill
        case 2:
            league_fill = league2_fill
        case 3:
            league_fill = league3_fill
        case 4:
            league_fill = league4_fill
        case _:
            league_fill = main_fill

    shift_y = 44

    name_x, name_y = 153, 464
    purpose_x, purpose_y = 251, name_y + shift_y * 1
    league_x, league_y = 160, name_y + shift_y * 2
    place_league_x, place_league_y = 320, name_y + shift_y * 3
    sub_x, sub_y = 260, name_y + shift_y * 4

    avatar_x, avatar_y = 48, 70

    boost_x, boost_y = 160, 790
    points_x, points_y = 495, 830
    stars_x, stars_y = 900, points_y

    shift_y = 52

    tasks_daily_x, tasks_daily_y = 820, 170
    tests_daily_x, tests_daily_y = 770, tasks_daily_y + shift_y * 1
    variants_daily_x, variants_daily_y = 860, tasks_daily_y + shift_y * 2

    tasks_x, tasks_y = tasks_daily_x, 410
    tests_x, tests_y = tests_daily_x, tasks_y + shift_y * 1
    variants_x, variants_y = variants_daily_x, tasks_y + shift_y * 2

    percent_test_x, percent_test_y = 1300, tests_y + 5
    percent_var_x, percent_var_y = 1300, variants_y + 2

    time_task_x, time_task_y = tasks_x, 666
    count_quests_x, count_quests_y = time_task_x + 245, 723

    random_str = str(uuid.uuid4())
    random_str = random_str[:10]

    image_avatar = Image.open(f'{info_student.get("avatar_image")}')
    image_room_stats.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

    draw.text((name_x, name_y), f'{info_student.get("name")}', fill=main_fill, font=font)
    draw.text((purpose_x, purpose_y), f'{info_student.get("purpose")}', fill=main_fill, font=font)
    draw.text((league_x, league_y), f'{info_league.get("title_league")}', fill=league_fill, font=font_league)
    draw.text((place_league_x, place_league_y), f'{info_league.get("place")}', fill=main_fill, font=font)
    draw.text((sub_x, sub_y), f'{info_student.get("status_sub")}', fill=main_fill, font=font)

    draw.text((tasks_daily_x, tasks_daily_y), f'{stats_daily_student.get("tasks_daily")}', fill=main_fill, font=font2)
    draw.text((tests_daily_x, tests_daily_y), f'{stats_daily_student.get("tests_daily")}', fill=main_fill, font=font2)
    draw.text((variants_daily_x, variants_daily_y), f'{stats_daily_student.get("variants_daily")}', fill=main_fill, font=font2)

    draw.text((tasks_x, tasks_y), f'{stats_general_student.get("tasks")}', fill=main_fill, font=font2)
    draw.text((tests_x, tests_y), f'{stats_general_student.get("tests")}', fill=main_fill, font=font2)
    draw.text((variants_x, variants_y), f'{stats_general_student.get("variants")}', fill=main_fill, font=font2)

    draw.text((percent_test_x, percent_test_y), f'{stats_general_student.get("percent_test")}', fill=main_fill, font=font2)
    draw.text((percent_var_x, percent_var_y), f'{stats_general_student.get("percent_var")}', fill=main_fill, font=font2)

    draw.text((time_task_x, time_task_y), f'{stats_general_student.get("time_task")}', fill=main_fill, font=font2)
    draw.text((count_quests_x, count_quests_y), f'{info_student.get("count_quests")}', fill=main_fill, font=font2)

    draw.text((boost_x, boost_y), f'{info_student.get("time_boost")}', fill=main_fill, font=font)

    draw.text((points_x, points_y), f'{info_student.get("points")}', fill=main_fill, font=font_count)
    draw.text((stars_x, stars_y), f'{info_student.get("stars")}', fill=main_fill, font=font_count)

    image_room_stats.save(f'./media/temp/{random_str}.png', quality=100)

    path = f'./media/temp/{random_str}.png'

    return path

async def create_table_leaders_image(info_all_students, league_id, prize_league):


    image_leaders_board = Image.open(f'./media/table_leaders/leaders_board_{league_id}.png')

    draw = ImageDraw.Draw(image_leaders_board)
    font = ImageFont.truetype('./font/Montserrat-Medium.ttf', size=64)

    name_x, name_y = 470, 365
    points_x, points_y = 1050, 365
    avatar_x, avatar_y = 300, 345

    prize_points_x, prize_points_y = 0, 0
    if league_id == 4:
        prize_item_x, prize_item_y = 1480, 340
        prize_count_item_x, prize_count_item_y = 1585, 410
    else:
        prize_points_x, prize_points_y = 1485, 365
        prize_item_x, prize_item_y = 1625, 340
        prize_count_item_x, prize_count_item_y = 1730, 410

    random_str = str(uuid.uuid4())
    random_str = random_str[:10]

    number = 0
    for student in info_all_students:
        number += 1
        if number < 3:
            if league_id == 1:
                prize_points = prize_league[number - 1][1]
                draw.text((prize_points_x, prize_points_y), f'{prize_points}', fill='white', font=font)
                prize_points_y += 291
            elif league_id == 4:
                prize_item_image = prize_league[number - 1][2]
                prize_item_count = prize_league[number - 1][3]

                image_item = Image.open(f'{prize_item_image}')
                image_leaders_board.paste(image_item, (prize_item_x, prize_item_y), mask=image_item)

                draw.text((prize_count_item_x, prize_count_item_y), f'x{prize_item_count}', fill='white', font=font)

                prize_item_y += 291
                prize_count_item_y += 291
            else:
                prize_points = prize_league[number - 1][1]
                prize_item_image = prize_league[number - 1][2]
                prize_item_count = prize_league[number - 1][3]

                draw.text((prize_points_x, prize_points_y), f'{prize_points}', fill='white', font=font)

                image_item = Image.open(f'{prize_item_image}')
                image_leaders_board.paste(image_item, (prize_item_x, prize_item_y), mask=image_item)

                draw.text((prize_count_item_x, prize_count_item_y), f'x{prize_item_count}', fill='white', font=font)

                prize_points_y += 291
                prize_item_y += 291
                prize_count_item_y += 291

            draw.text((name_x, name_y), f'{student[0]}', fill='white', font=font)
            draw.text((points_x, points_y), f'{student[1]}', fill='white', font=font)

            image_id = student[2]
            image_avatar = Image.open(f'{image_id}')
            image_leaders_board.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

            name_y += 291
            points_y += 291
            avatar_y += 291
        elif number == 3:
            if league_id == 1:
                prize_points = prize_league[number - 1][1]
                draw.text((prize_points_x, prize_points_y), f'{prize_points}', fill='white', font=font)
                prize_points_y += 323
            elif league_id == 4:
                prize_item_image = prize_league[number - 1][2]
                prize_item_count = prize_league[number - 1][3]

                image_item = Image.open(f'{prize_item_image}')
                image_leaders_board.paste(image_item, (prize_item_x, prize_item_y), mask=image_item)

                draw.text((prize_count_item_x, prize_count_item_y), f'x{prize_item_count}', fill='white', font=font)

                prize_item_y += 323
                prize_count_item_y += 323
            else:
                prize_points = prize_league[number - 1][1]
                prize_item_image = prize_league[number - 1][2]
                prize_item_count = prize_league[number - 1][3]

                draw.text((prize_points_x, prize_points_y), f'{prize_points}', fill='white', font=font)

                image_item = Image.open(f'{prize_item_image}')
                image_leaders_board.paste(image_item, (prize_item_x, prize_item_y), mask=image_item)

                draw.text((prize_count_item_x, prize_count_item_y), f'x{prize_item_count}', fill='white', font=font)

                prize_points_y += 323
                prize_item_y += 323
                prize_count_item_y += 323

            draw.text((name_x, name_y), f'{student[0]}', fill='white', font=font)
            draw.text((points_x, points_y), f'{student[1]}', fill='white', font=font)

            image_id = student[2]
            image_avatar = Image.open(f'{image_id}')
            image_leaders_board.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

            name_y += 323
            points_y += 323
            avatar_y += 323
        else:
            if league_id == 4:
                prize_item_image = prize_league[3][2]
                prize_item_count = prize_league[3][3]

                image_item = Image.open(f'{prize_item_image}')
                image_leaders_board.paste(image_item, (prize_item_x, prize_item_y), mask=image_item)

                draw.text((prize_count_item_x, prize_count_item_y), f'x{prize_item_count}', fill='white', font=font)

                prize_item_y += 226
                prize_count_item_y += 226
            else:
                prize_points = prize_league[3][1]
                draw.text((prize_points_x, prize_points_y), f'{prize_points}', fill='white', font=font)
                prize_points_y += 226

            draw.text((name_x, name_y), f'{student[0]}', fill='white', font=font)
            draw.text((points_x, points_y), f'{student[1]}', fill='white', font=font)

            image_id = student[2]
            image_avatar = Image.open(f'{image_id}')
            image_leaders_board.paste(image_avatar, (avatar_x, avatar_y), mask=image_avatar)

            name_y += 226
            points_y += 226
            avatar_y += 226

    image_leaders_board.save(f'./media/{random_str}.png', quality=100)

    path = f'./media/{random_str}.png'

    return path