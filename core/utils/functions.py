
import datetime
import calendar

async def get_int_time(current_time):
    time = str(current_time)
    time = time[11:19]
    int_time = int(time[0:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8])
    print(int_time)
    return int_time

async def get_task_completion_time(time_answer):
    if time_answer < 60:
        bot_time_answer = f"🤖: Время выполнения: {time_answer} сек."
    elif time_answer < 3600:
        min = time_answer // 60
        sec = time_answer - min * 60
        bot_time_answer = f"🤖: Время выполнения: {min} мин. {sec} сек."
    else:
        hour = time_answer // 3600
        min = (time_answer - hour * 3600) // 60
        sec = time_answer - min * 60 - hour * 3600
        bot_time_answer = f"🤖: Время выполнения: {hour} ч. {min} мин. {sec} сек."

    return bot_time_answer


async def generate_date_update_league():

    current_date = datetime.datetime.today()

    date = str(current_date)
    month = date[5:7]
    year = date[0:4]
    last_day_month = calendar.monthrange(int(year), int(month))[1]
    first_day_month = calendar.monthrange(int(year), int(month))[0]

    last_day_date = datetime.datetime(int(year), int(month), last_day_month, 18)
    first_day_date = datetime.datetime(int(year), int(month), first_day_month, 18)

    list_date = []
    interval_update_league_days = 3
    current_date = first_day_date

    while current_date < last_day_date:
        current_date += datetime.timedelta(days=interval_update_league_days)
        list_date.append(current_date)

    if (last_day_date-list_date[-1]).days < interval_update_league_days:
        list_date.pop(-1)

    print(list_date, last_day_date)

    return list_date, last_day_date

async def get_hours_update_league():
    current_date = datetime.datetime.today()
    list_date, last_day_date = await generate_date_update_league()

    new_date = datetime.datetime.today()

    for date in list_date:
        if current_date > date:
            continue
        else:
            new_date = date - current_date
            break

    if list_date[-1] < current_date < last_day_date:
        new_date = last_day_date - current_date

    dif_sec = new_date.seconds + new_date.days * 3600 * 24
    dif_hours = int(round(dif_sec / 3600, 0))

    return dif_hours


async def check_date_update_league():
    current_date = datetime.datetime.today().date()
    list_date, last_day_date = await generate_date_update_league()
    checker = False
    for date in list_date:
        if current_date == date.date():
            checker = True

    return checker






