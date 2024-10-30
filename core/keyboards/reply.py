from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_BUTTON_main_menu, LEXICON_BUTTON_solve_menu, \
    LEXICON_BUTTON_back_menu, LEXICON_BUTTON_theory_menu, LEXICON_BUTTON_UTC


async def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for key in LEXICON_BUTTON_main_menu:
        builder.button(text=LEXICON_BUTTON_main_menu[key])
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup(resize_keyboard=True)

async def solve_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for key in LEXICON_BUTTON_solve_menu:
        builder.button(text=LEXICON_BUTTON_solve_menu[key])
    builder.button(text=LEXICON_BUTTON_back_menu["back_menu"])
    builder.adjust(2, 1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)

async def theory_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for key in LEXICON_BUTTON_theory_menu:
        builder.button(text=LEXICON_BUTTON_theory_menu[key])
    builder.button(text=LEXICON_BUTTON_back_menu["back_solve"])
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)

async def time_utc_keyboard():
    builder = ReplyKeyboardBuilder()
    for key in LEXICON_BUTTON_UTC:
        builder.button(text=LEXICON_BUTTON_UTC[key])
    builder.button(text=LEXICON_BUTTON_back_menu["back_solve"])
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["solve"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["quests"]),
            KeyboardButton(text=LEXICON_BUTTON["my_backpack"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["shop"]),
            KeyboardButton(text=LEXICON_BUTTON["my_room"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["info"]),
            KeyboardButton(text=LEXICON_BUTTON["table_leaders"])
        ]
    ],
    resize_keyboard=True
)

solve_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["solve_tasks"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["solve_variant"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["solve_daily_task"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ],
    resize_keyboard=True
)

solve_tasks_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["random_task"]),
            KeyboardButton(text=LEXICON_BUTTON["specific_task"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["test"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back"])
        ]
    ],
    resize_keyboard=True
)

solve_variants_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["random_variant"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["weekly_variant"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back"])
        ]
    ],
    resize_keyboard=True
)

back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ],
    resize_keyboard=True
)

back_solve = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back"])
        ]
    ],
    resize_keyboard=True
)

back_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_info"])
        ]
    ],
    resize_keyboard=True
)


choose_purpose_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["purpose_1"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["purpose_2"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["purpose_3"]),
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["purpose_4"])
        ]
    ],
    resize_keyboard=True
)

room_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["my_backpack"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["stats_for_tasks"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["room_settings"]),
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["back_room"])
        ]
    ],
    resize_keyboard=True
)

room_settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["change_name"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["change_purpose"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["back_room"])
        ]
    ],
    resize_keyboard=True
)

info_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["info_sub"]),
            KeyboardButton(text=LEXICON_BUTTON["invite_friends"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["help"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ],
    resize_keyboard=True
)

shop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["shop_cases"]),
            KeyboardButton(text=LEXICON_BUTTON["shop_sub"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["shop_leaders"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ],
    resize_keyboard=True
)

next_task = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["resolve_task"]),
            KeyboardButton(text=LEXICON_BUTTON["check_solution"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back"]),
            KeyboardButton(text=LEXICON_BUTTON["next_task"])
        ]
    ],
    resize_keyboard=True
)

end_daily_task = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["check_solution"]),
            KeyboardButton(text=LEXICON_BUTTON["back"])
        ]
    ],
    resize_keyboard=True
)

next_task_in_test = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["next_task"])
        ]
    ],
    resize_keyboard=True
)

view_results = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["view_results"])
        ]
    ],
    resize_keyboard=True
)

results_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["check_solution"])
        ]
    ],
    resize_keyboard=True
)


begin_solve_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back"]),
            KeyboardButton(text=LEXICON_BUTTON["begin_solve"])
        ]
    ],
    resize_keyboard=True
)

open_case_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"]),
            KeyboardButton(text=LEXICON_BUTTON["my_backpack"])
        ]
    ],
    resize_keyboard=True
)


tasks_selection_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4")
        ],
        [
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
            KeyboardButton(text="7"),
            KeyboardButton(text="8")
        ],
        [
            KeyboardButton(text="9"),
            KeyboardButton(text="10"),
            KeyboardButton(text="11"),
            KeyboardButton(text="12")
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ],
    ],
    resize_keyboard=True
)

help_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["report_error"]),
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["faq"]),
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_info"])
        ],
    ],
    resize_keyboard=True
)

faq_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["ask_question"]),
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_info"])
        ],
    ],
    resize_keyboard=True
)



