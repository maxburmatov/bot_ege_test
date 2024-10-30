from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from enum import IntEnum, auto

from core.lexicon.lexicon import LEXICON_BUTTON


class BackpackCategory(IntEnum):
    avatars = auto()
    cases = auto()
    other = auto()
    main = auto()

class BackpackAction(IntEnum):
    change_avatar = auto()
    open_case = auto()
    use_boost = auto()
    skip = auto()

class BackpackCallback(CallbackData, prefix="bp"):
    category: BackpackCategory
    action: BackpackAction
    page: int


async def get_main_backpack_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LEXICON_BUTTON["backpack_avatars"],
        callback_data=BackpackCallback(page=page, category=BackpackCategory.avatars, action=BackpackAction.skip)
    )

    builder.button(
        text=LEXICON_BUTTON["backpack_cases"],
        callback_data=BackpackCallback(page=page, category=BackpackCategory.cases, action=BackpackAction.skip)
    )

    builder.button(
        text=LEXICON_BUTTON["backpack_other"],
        callback_data=BackpackCallback(page=page, category=BackpackCategory.other, action=BackpackAction.skip)
    )

    builder.adjust(1)

    return builder.as_markup()

async def get_avatars_backpack_keyboard(page: int = 0, count: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count_item = count
    has_next_page = count_item > page + 1

    if page != 0:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data=BackpackCallback(page=page - 1, category=BackpackCategory.avatars, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data="dont_click_me!"
        )

    if has_next_page:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data=BackpackCallback(page=page + 1, category=BackpackCategory.avatars, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data="dont_click_me!"
        )

    builder.button(
        text=LEXICON_BUTTON["back"],
        callback_data=BackpackCallback(page=0, category=BackpackCategory.main, action=BackpackAction.skip)
    )
    builder.button(
        text="Поставить этот аватар",
        callback_data=BackpackCallback(page=page, category=BackpackCategory.avatars, action=BackpackAction.change_avatar)
    )

    builder.adjust(2)

    return builder.as_markup()

async def get_cases_backpack_keyboard(page: int = 0, count: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count_item = count
    has_next_page = count_item > page + 1

    if page != 0:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data=BackpackCallback(page=page - 1, category=BackpackCategory.cases, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data="dont_click_me!"
        )

    if has_next_page:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data=BackpackCallback(page=page + 1, category=BackpackCategory.cases, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data="dont_click_me!"
        )

    builder.button(
        text=LEXICON_BUTTON["back"],
        callback_data=BackpackCallback(page=0, category=BackpackCategory.main, action=BackpackAction.skip)
    )

    builder.button(
        text="Открыть кейс!",
        callback_data=BackpackCallback(page=page, category=BackpackCategory.cases, action=BackpackAction.open_case)
    )

    builder.adjust(2)

    return builder.as_markup()

async def get_other_backpack_keyboard(page: int = 0, count: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count_item = count
    has_next_page = count_item > page + 1

    if page != 0:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data=BackpackCallback(page=page - 1, category=BackpackCategory.other, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["prev"],
            callback_data="dont_click_me!"
        )

    if has_next_page:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data=BackpackCallback(page=page + 1, category=BackpackCategory.other, action=BackpackAction.skip)
        )
    else:
        builder.button(
            text=LEXICON_BUTTON["next"],
            callback_data="dont_click_me!"
        )

    builder.button(
        text=LEXICON_BUTTON["back"],
        callback_data=BackpackCallback(page=0, category=BackpackCategory.main, action=BackpackAction.skip)
    )

    builder.button(
        text="Использовать",
        callback_data=BackpackCallback(page=page, category=BackpackCategory.other, action=BackpackAction.use_boost)
    )

    builder.adjust(2)

    return builder.as_markup()