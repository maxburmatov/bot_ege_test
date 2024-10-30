from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from enum import IntEnum, auto

from core.database.metods.shop import get_shop_case
from core.lexicon.lexicon import LEXICON_BUTTON


class ShopActions(IntEnum):
    buy = auto()
    choose = auto()


class BuyItemsCount(IntEnum):
    skip = auto()
    one = auto()
    five = auto()
    twenty = auto()


class CasesCallback(CallbackData, prefix="cases"):
    action: ShopActions
    page: int
    item_count: BuyItemsCount


async def get_shop_cases_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count_cases, info_case = await get_shop_case(page)
    cases_data = info_case["cases_data"]
    price_case_x1 = cases_data[0][4]
    price_case_x5 = cases_data[1][4]
    price_case_x20 = cases_data[2][4]

    has_next_page = count_cases > page + 1

    builder.row(
        types.InlineKeyboardButton(text=f"Купить x1 за ⭐️ {price_case_x1}",
                                   callback_data=CasesCallback(page=page, action=ShopActions.buy,
                                                               item_count=BuyItemsCount.one).pack()),
        types.InlineKeyboardButton(text=f"Купить x5 за ⭐️ {price_case_x5}",
                                   callback_data=CasesCallback(page=page, action=ShopActions.buy,
                                                               item_count=BuyItemsCount.five).pack()),
        types.InlineKeyboardButton(text=f"Купить x20 за ⭐️ {price_case_x20}",
                                   callback_data=CasesCallback(page=page, action=ShopActions.buy,
                                                               item_count=BuyItemsCount.twenty).pack()),
        types.InlineKeyboardButton(text=f"[{page + 1}/{count_cases}]", callback_data="dont_click_me"),
        width=1
    )

    if page != 0 and has_next_page:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data=CasesCallback(page=page - 1, action=ShopActions.choose,
                                                                   item_count=BuyItemsCount.skip).pack()),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data=CasesCallback(page=page + 1, action=ShopActions.choose,
                                                                   item_count=BuyItemsCount.skip).pack()),
            width=2
        )
    elif page == 0 and has_next_page:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data="dont_click_me"),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data=CasesCallback(page=page + 1, action=ShopActions.choose,
                                                                   item_count=BuyItemsCount.skip).pack()),
            width=2
        )
    else:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data=CasesCallback(page=page - 1, action=ShopActions.choose,
                                                                   item_count=BuyItemsCount.skip).pack()),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data="dont_click_me"),
            width=2
        )

    return builder.as_markup()
