from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from enum import IntEnum, auto

from core.database.admin_metods import get_request, get_count_type_request
from core.database.metods.shop import get_shop_case
from core.lexicon.lexicon import LEXICON_BUTTON


class RequestStatus(IntEnum):
    new = auto()
    finished = auto()


class RequestType(IntEnum):
    question = auto()
    error = auto()
    error_task = auto()


class RequestAction(IntEnum):
    answer_user = auto()
    mark_spam = auto()
    mark_finished = auto()
    choose = auto()
    main = auto()


class RequestCallback(CallbackData, prefix="request"):
    type_request: RequestType
    status: RequestStatus
    action: RequestAction
    page: int


async def get_type_requests_keyboard(page: int = 0, status_request: str = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    count_request = await get_count_type_request(status_request)

    if status_request == "new":
        status_request = 1
    else:
        status_request = 2

    builder.button(
        text=f"question({count_request.get("count_question_request")})",
        callback_data=RequestCallback(page=page, status=status_request, action=RequestAction.choose,
                                      type_request=RequestType.question)
    )

    builder.button(
        text=f"error({count_request.get("count_error_request")})",
        callback_data=RequestCallback(page=page, status=status_request, action=RequestAction.choose,
                                      type_request=RequestType.error)
    )

    builder.button(
        text=f"error_task({count_request.get("count_error_task_request")})",
        callback_data=RequestCallback(page=page, status=status_request, action=RequestAction.choose,
                                      type_request=RequestType.error_task)
    )

    builder.adjust(1)

    return builder.as_markup()


async def get_requests_keyboard(page: int = 0, count: int = 0, status: int = 0, type_request: int = 0) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    has_next_page = count > page + 1

    if status == 1:
        builder.row(
            types.InlineKeyboardButton(text=LEXICON_BUTTON["answer_user"],
                                       callback_data=RequestCallback(page=page, action=RequestAction.answer_user,
                                                                     type_request=type_request, status=status).pack()),
            types.InlineKeyboardButton(text=LEXICON_BUTTON["mark_spam"],
                                       callback_data=RequestCallback(page=page, action=RequestAction.mark_spam,
                                                                     type_request=type_request, status=status).pack()),
            types.InlineKeyboardButton(text=LEXICON_BUTTON["mark_finished"],
                                       callback_data=RequestCallback(page=page, action=RequestAction.mark_finished,
                                                                     type_request=type_request, status=status).pack()),
            types.InlineKeyboardButton(text=f"[{page + 1}/{count}]", callback_data="dont_click_me"),
            types.InlineKeyboardButton(text=LEXICON_BUTTON["back_type"],
                                       callback_data=RequestCallback(page=page, action=RequestAction.main,
                                                                     type_request=type_request, status=status).pack()),
            width=1
        )

    if status == 2:
        builder.row(
            types.InlineKeyboardButton(text=f"[{page + 1}/{count}]", callback_data="dont_click_me"),
            types.InlineKeyboardButton(text=LEXICON_BUTTON["back_type"],
                                       callback_data=RequestCallback(page=page, action=RequestAction.main,
                                                                     type_request=type_request, status=status).pack()),
            width=1
        )

    if page != 0 and has_next_page:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data=RequestCallback(page=page - 1, action=RequestAction.choose,
                                                                     type_request=type_request, status=status).pack()),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data=RequestCallback(page=page + 1, action=RequestAction.choose,
                                                                     type_request=type_request, status=status).pack()),
            width=2
        )
    elif page == 0 and has_next_page:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data="dont_click_me"),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data=RequestCallback(page=page + 1, action=RequestAction.choose,
                                                                     type_request=type_request, status=status).pack()),
            width=2
        )
    else:
        builder.row(
            types.InlineKeyboardButton(text="⬅️",
                                       callback_data=RequestCallback(page=page - 1, action=RequestAction.choose,
                                                                     type_request=type_request, status=status).pack()),
            types.InlineKeyboardButton(text="➡️",
                                       callback_data="dont_click_me"),
            width=2
        )

    return builder.as_markup()
