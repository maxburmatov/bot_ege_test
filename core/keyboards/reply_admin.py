from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from core.database.admin_metods import get_count_new_request, get_count_status_request

from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_BUTTON_main_menu


async def get_admin_panel():
    count_request = await get_count_new_request()
    kb_list = [
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_stats"]),
            KeyboardButton(text=LEXICON_BUTTON["admin_users"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_edit"]),
            KeyboardButton(text=LEXICON_BUTTON["admin_send"])
        ],
        [
            KeyboardButton(text=f"{LEXICON_BUTTON["admin_request"]} ({count_request})")
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

async def get_admin_request_keyboard():
    count_request = await get_count_status_request()
    kb_list = [
        [
            KeyboardButton(text=f"{LEXICON_BUTTON["admin_new_request"]}({count_request.get("count_new_request")})")
        ],
        [
            KeyboardButton(text=f"{LEXICON_BUTTON["admin_finished_request"]}({count_request.get("count_finished_request")})")
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_admin_panel"])
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

async def main_menu_keyboard_admin():
    builder = ReplyKeyboardBuilder()
    for key in LEXICON_BUTTON_main_menu:
        builder.button(text=LEXICON_BUTTON_main_menu[key])
    builder.button(text=LEXICON_BUTTON["admin_panel"])
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)

admin_stats_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_stats"]),
            KeyboardButton(text=LEXICON_BUTTON["admin_users"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_edit"]),
            KeyboardButton(text=LEXICON_BUTTON["admin_send"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_menu"])
        ]
    ],
    resize_keyboard=True
)


admin_edit_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_edit_task"]),
            KeyboardButton(text=LEXICON_BUTTON["admin_add_task"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_add_var"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["admin_add_quest"])
        ],
        [
            KeyboardButton(text=LEXICON_BUTTON["back_admin_panel"])
        ]
    ],
    resize_keyboard=True
)

back_admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_admin_panel"])
        ]
    ],
    resize_keyboard=True
)



back_admin_request = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=LEXICON_BUTTON["back_admin_request"])
        ],
    ],
    resize_keyboard=True
)