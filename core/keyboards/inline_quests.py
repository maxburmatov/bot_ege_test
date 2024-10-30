from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from enum import IntEnum, auto

from core.lexicon.lexicon import LEXICON_BUTTON


class QuestsCategory(IntEnum):
    daily_bonus = auto()
    daily_quests = auto()
    other_quests = auto()
    main = auto()

class QuestsAction(IntEnum):
    check_execution = auto()
    collect_bonus = auto()
    skip = auto()

class QuestsCallback(CallbackData, prefix="que"):
    category: QuestsCategory
    action: QuestsAction


async def get_main_quests_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LEXICON_BUTTON["daily_bonus"],
        callback_data=QuestsCallback(category=QuestsCategory.daily_bonus, action=QuestsAction.skip)
    )

    builder.button(
        text=LEXICON_BUTTON["quests_daily"],
        callback_data=QuestsCallback(category=QuestsCategory.daily_quests, action=QuestsAction.skip)
    )

    builder.button(
        text=LEXICON_BUTTON["quests_other"],
        callback_data=QuestsCallback(category=QuestsCategory.other_quests, action=QuestsAction.skip)
    )

    builder.adjust(1)

    return builder.as_markup()

async def get_quests_keyboard(category: str = "") -> InlineKeyboardMarkup:
    if category == "daily":
        category = 2
    elif category == "other":
        category = 3
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LEXICON_BUTTON["quests_check"],
        callback_data=QuestsCallback(category=category, action=QuestsAction.check_execution)
    )

    builder.button(
        text=LEXICON_BUTTON["back"],
        callback_data=QuestsCallback(category=QuestsCategory.main, action=QuestsAction.skip)
    )

    builder.adjust(1)
    
    return builder.as_markup()


async def get_daily_bonus_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LEXICON_BUTTON["collect_daily_bonus"],
        callback_data=QuestsCallback(category=QuestsCategory.daily_bonus, action=QuestsAction.collect_bonus)
    )

    builder.button(
        text=LEXICON_BUTTON["back"],
        callback_data=QuestsCallback(category=QuestsCategory.main, action=QuestsAction.skip)
    )

    builder.adjust(1)

    return builder.as_markup()

