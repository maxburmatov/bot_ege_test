
async def ending_hours(hours):
    text_hour = ""
    if hours > 9:
        hours = hours % 10
    match hours:
        case 1:
            text_hour = "час"
        case 2 | 3 | 4:
            text_hour = "часа"
        case _:
            text_hour = "часов"

    return text_hour